from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
import os
import shutil
import zipfile
import requests
import socket
from run_workflow import run_codegen_workflow
from uuid import uuid4

app = FastAPI()
UPLOAD_DIR = "uploaded_docs"
OUTPUT_DIR = "generated_code"
ZIP_DIR = "zipped_output"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ZIP_DIR, exist_ok=True)

def get_free_port():
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

@app.post("/upload")
async def upload_doc(file: UploadFile = File(...)):
    if not file.filename.endswith(".docx"):
        return JSONResponse(status_code=400, content={"error": "Only .docx files are allowed."})
    
    uid = str(uuid4())
    saved_path = os.path.join(UPLOAD_DIR, f"{uid}.docx")
    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    final_state = run_codegen_workflow(saved_path, OUTPUT_DIR)
    
    zip_path = os.path.join(ZIP_DIR, f"{uid}.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, _, files in os.walk(OUTPUT_DIR):
            for filename in files:
                filepath = os.path.join(root, filename)
                arcname = os.path.relpath(filepath, OUTPUT_DIR)
                zipf.write(filepath, arcname=arcname)

    port = get_free_port()
    container_url = f"http://localhost:{port}"
    container_id = build_and_run_podman_container(OUTPUT_DIR, port)

    endpoints = []
    try:
        import time
        time.sleep(2)  # Give container a moment to start
        resp = requests.get(f"{container_url}/openapi.json")
        if resp.ok:
            data = resp.json()
            endpoints = [path for path in data.get("paths", {}).keys()]
    except Exception as e:
        endpoints = ["Could not fetch OpenAPI schema"]

    return {
        "message": "SRS processed successfully",
        "download_url": f"/download/{uid}",
        "live_url": container_url,
        "endpoints": endpoints
    }

@app.get("/download/{uid}")
def download_zip(uid: str):
    zip_path = os.path.join(ZIP_DIR, f"{uid}.zip")
    if os.path.exists(zip_path):
        return FileResponse(zip_path, media_type="application/zip", filename=f"{uid}.zip")
    return {"error": "File not found"}

def build_and_run_podman_container(code_dir, port):
    dockerfile_path = os.path.join(code_dir, "Dockerfile")
    with open(dockerfile_path, "w") as f:
        f.write(f"""
        FROM python:3.10-slim
        WORKDIR /app
        COPY . .
        RUN pip install fastapi uvicorn
        CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
        """)

    image_name = f"fastapi-generated-{uuid4().hex[:6]}"
    os.system(f"podman build -t {image_name} {code_dir}")
    run_cmd = f"podman run -d -p {port}:8080 {image_name}"
    container_id = os.popen(run_cmd).read().strip()
    return container_id

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
