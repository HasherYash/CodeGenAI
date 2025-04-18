import os
import zipfile
from langgraph_workflow import traceable, CodeState

@traceable(name="ZipProject")
def zip_node(state: CodeState) -> CodeState:
    project_dir = state.get("project_dir")

    if not project_dir or not os.path.exists(project_dir):
        raise ValueError("Project directory not found for zipping.")

    # Create output folder if not exists
    output_dir = os.path.join(os.getcwd(), "output_zip")
    os.makedirs(output_dir, exist_ok=True)

    # Define zip file name
    zip_name = f"{state.get('project_name', 'fastapi_project')}.zip"
    zip_path = os.path.join(output_dir, zip_name)

    # Create zip archive
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, project_dir)
                zipf.write(full_path, arcname=rel_path)

    # Save path to zip in state
    state["zip_path"] = zip_path
    state["zip_created"] = True
    print(f"Project zipped at: {zip_path}")

    return state
