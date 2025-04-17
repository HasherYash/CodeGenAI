import os
def build_and_run_podman_container(code_dir: str):
   dockerfile_path = os.path.join(code_dir, "Dockerfile")
   with open(dockerfile_path, "w") as f:
       f.write("""
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
""")
   os.system(f"podman build -t fastapi-generated {code_dir}")
   os.system("podman run -d -p 8080:8080 fastapi-generated")