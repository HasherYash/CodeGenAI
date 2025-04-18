import os
from langgraph_workflow import traceable, CodeState, llm

@traceable(name="TestGen")

def testgen_node(state: CodeState) -> CodeState:

    project_dir = state.get("project_dir")
    raw_code = state.get("generated_code")

    prompt = f"""

        You are a senior Python test engineer. Write `pytest` unit tests for the following FastAPI app code:

        {raw_code}

        Make sure to:

        - Cover route handlers with FastAPI TestClient or async client.
        - Validate Pydantic models with example inputs.
        - Test service logic including edge cases.
        - Organize tests into appropriate functions.
        - Use clear assertions.
        - Avoid hardcoding values where possible.
        - Output only test code. Do not add explanations.

        """

    # Generate tests
    response = llm.invoke(prompt)
    test_code = response.content

    # Save to tests/test_generated.py
    test_dir = os.path.join(project_dir, "tests")
    os.makedirs(test_dir, exist_ok=True)
    test_file_path = os.path.join(test_dir, "test_generated.py")

    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(test_code)

    state["generated_tests"] = test_code
    # Return updated state
    return state

