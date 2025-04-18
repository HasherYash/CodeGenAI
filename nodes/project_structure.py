import os
import uuid
from typing import Dict, List
from langgraph_workflow import traceable, CodeState

file_name =""
@traceable(name="PrepareProject")
def prepare_project_structure_node(state: CodeState) -> CodeState:
    """Create the full project directory and subdirectories as per parsed SRS structure."""

    # Create a unique base project folder
    base_dir = os.path.join("generated_code", f"project_{uuid.uuid4()}")
    file_name = f"project_{uuid.uuid4()}"
    os.makedirs(base_dir, exist_ok=True)

    # Extract structured file info from state (provided by LLM in ParseSRS)
    project_structure: Dict[str, List[str]] = state.get("project_structure_plan", {})

    # Create folders and files as per parsed structure
    for folder, files in project_structure.items():
        folder_path = os.path.join(base_dir, folder)
        os.makedirs(folder_path, exist_ok=True)
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            open(file_path, "w").close()

    # Save base path to state
    state["project_dir"] = base_dir

    return state
