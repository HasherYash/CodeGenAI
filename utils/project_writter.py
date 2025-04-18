import os

def write_project_structure(base_dir: str, code: str, tests: str) -> str:

    """

    Write FastAPI project code and tests into a clean directory structure.

    Structure:
    base_dir/
        app/
            main.py
        tests/
            test_main.py
        README.md
        openapi.json
        api_diagram.mmd

    """

    app_dir = os.path.join(base_dir, "app")
    test_dir = os.path.join(base_dir, "tests")
    os.makedirs(app_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # Write main code
    with open(os.path.join(app_dir, "main.py"), "w") as f:
        f.write(code)

    # Write tests
    with open(os.path.join(test_dir, "test_main.py"), "w") as f:
        f.write(tests)

    return base_dir 