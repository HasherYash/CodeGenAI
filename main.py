from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from run_workflow import run_codegen_workflow
from uuid import uuid4
import os
import shutil
import zipfile

app = FastAPI()

UPLOAD_DIR = "uploaded_docs"
OUTPUT_DIR = "generated_code"
ZIP_DIR = "zipped_output"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ZIP_DIR, exist_ok=True)

@app.post("/upload")
async def upload_doc(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.endswith(".docx"):
        return JSONResponse(status_code=400, content={"error": "Only .docx files are allowed."})

    # Unique filename
    uid = str(uuid4())
    saved_path = os.path.join(UPLOAD_DIR, f"{uid}.docx")

    # Save uploaded file
    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Trigger LangGraph workflow
    run_codegen_workflow(saved_path, OUTPUT_DIR) 

    # Zip the output
    zip_path = os.path.join(ZIP_DIR, f"{uid}.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, _, files in os.walk(OUTPUT_DIR):
            for filename in files:
                filepath = os.path.join(root, filename)
                arcname = os.path.relpath(filepath, OUTPUT_DIR)
                zipf.write(filepath, arcname=arcname)

    # Optionally: run the generated FastAPI project via Podman
    build_and_run_podman_container(OUTPUT_DIR) 
    return {"message": "SRS processed successfully", "download_url": f"/download/{uid}"} 

@app.get("/download/{uid}")
def download_zip(uid: str):
    zip_path = os.path.join(ZIP_DIR, f"{uid}.zip")
    if os.path.exists(zip_path):
        return FileResponse(zip_path, media_type="application/zip", filename=f"{uid}.zip")
    return {"error": "File not found"} 

def build_and_run_podman_container(code_dir):
    podmanfile = os.path.join(code_dir, "Dockerfile")
    with open(podmanfile, "w") as f:
        f.write(f"""

FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

""")

    os.system(f"podman build -t fastapi-generated {code_dir}")
    os.system("podman run -d -p 8080:8080 fastapi-generated") 