from langgraph_workflow import build_langgraph

from utils.podman_runner import build_and_run_podman_container

import tempfile

import os

# Set path to your .docx SRS file

SRS_FILE_PATH = "sample_srs.docx"

# Build the workflow

workflow = build_langgraph()

# Define the starting state

initial_state = {"srs_path": SRS_FILE_PATH}

# Run the workflow

final_state = workflow.invoke(initial_state)

# Extract the generated code

generated_code = final_state.get("generated_code", {}).get("raw", "")

if not generated_code:

    print("No code generated.")

    exit()

# Save the generated code to a temporary directory

with tempfile.TemporaryDirectory() as temp_dir:

    main_path = os.path.join(temp_dir, "main.py")

    with open(main_path, "w", encoding="utf-8") as f:

        f.write(generated_code)

    # === RUN GENERATED CODE USING PODMAN ===

    print("[Podman] Building and running container with generated code...")

    build_and_run_podman_container(temp_dir)

    print("Visit http://localhost:8080/docs to test the generated API") 