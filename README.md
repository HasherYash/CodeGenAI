# CodeGenAI

# FastAPI Code Generation Workflow

This project is a FastAPI application that allows users to upload `.docx` files, processes them using a code generation workflow, and provides the generated code as a downloadable zip file. Additionally, it runs the generated code in a Podman container and exposes the API endpoints.

## Features

- Upload `.docx` files
- Process files using a code generation workflow
- Download the generated code as a zip file
- Run the generated code in a Podman container
- Expose API endpoints from the generated code

## Requirements

- Python 3.10
- FastAPI
- Uvicorn
- Podman
- Requests
- Python-dotenv

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/fastapi-codegen-workflow.git
    cd fastapi-codegen-workflow
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Ensure Podman is installed and running on your system.

## Environment Variables

Create a `.env` file in the root directory of the project and add any necessary environment variables. For example:

```env
# .env
SOME_ENV_VARIABLE=your_value
