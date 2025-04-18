import os
from langgraph_workflow import traceable, CodeState, llm

@traceable(name="GenerateDocs")
def generate_docs_node(state: CodeState) -> CodeState:

    project_dir = state.get("project_dir")
    code = state.get("generated_code")

    # if not project_dir or not code:
    #     raise ValueError("Missing project_dir or generated code")
    prompt = f"""You are a technical documentation expert.
        Based on the following FastAPI code, generate:
        1. A detailed README.md explaining setup, usage, endpoints.
        2. A simplified OpenAPI spec in JSON.
        3. A Mermaid diagram (markdown-friendly) of the API structure.

        returns a structured response everthing in sepret block

        Code:{code}
        """

    response = llm.invoke(prompt)


    docs_path = os.path.join(project_dir, "docs")
    os.makedirs(docs_path, exist_ok=True)

    # For example purposes, writing the full response to all docs

    with open(os.path.join(docs_path, "README.md"), "w") as f:
        f.write(response.content)

    with open(os.path.join(docs_path, "openapi.json"), "w") as f:
        f.write(response.content)

    with open(os.path.join(docs_path, "api_diagram.mmd"), "w") as f:
        f.write(response.content)

    state["docs_generated"] = True

    return state 