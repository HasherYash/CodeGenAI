import os
from langchain_core.runnables import Runnable
from langgraph_workflow import traceable, CodeState, llm

@traceable(name="CodeGen")
def codegen_node(state: CodeState) -> CodeState:
    extracted_info = state.get("extracted_info", {})
    project_root = state.get("project_dir", "")
    project_structure = state.get("project_structure_plan", {})

    if not project_root:
        raise ValueError("Project directory not found in state.")

    # Create directory structure
    dirs = {
        "models": os.path.join(project_root, "models"),
        "routers": os.path.join(project_root, "routers"),
        "services": os.path.join(project_root, "services"),
        "app": os.path.join(project_root, "app")
    }

    for dir_path in dirs.values():
        os.makedirs(dir_path, exist_ok=True)

    # Generate code using LLM for each part
    generated_code = {}

    # 1. Generate models
    model_prompt = f"""
    You are a Python backend developer. Generate Pydantic models based on the following entities:
    {extracted_info}
    Only return Python code, don't add any extra explanation to avoid errors.
    """
    models_code = llm.invoke(model_prompt).content
    generated_code["models"] = models_code

    with open(os.path.join(dirs["models"], "models.py"), "w", encoding="utf-8") as f:
        f.write(models_code)

    # 2. Generate routers
    router_prompt = f"""
    {models_code}
    Based on the following endpoints, generate FastAPI routers. Use APIRouter and organize properly.
    {extracted_info}
    Only return Python code, don't add any extra explanation to avoid errors.
    """
    routers_code = llm.invoke(router_prompt).content
    generated_code["routers"] = routers_code

    with open(os.path.join(dirs["routers"], "users.py"), "w", encoding="utf-8") as f:
        f.write(routers_code)

    # 3. Generate service logic
    service_prompt = f"""
    {models_code} and {routers_code}
    Based on the following business logic description, generate the service layer.
    {extracted_info}
    Only return Python code, don't add any extra explanation to avoid errors.
    """
    services_code = llm.invoke(service_prompt).content
    generated_code["services"] = services_code

    with open(os.path.join(dirs["services"], "user_service.py"), "w", encoding="utf-8") as f:
        f.write(services_code)

    # 4. Generate main.py
    main_prompt = f"""
    {models_code}, {routers_code} and {services_code}
    Generate the main.py file that initializes FastAPI app, includes routers, and runs the server.
    Only return Python code, don't add any extra explanation to avoid errors.
    """
    main_code = llm.invoke(main_prompt).content
    generated_code["main"] = main_code

    with open(os.path.join(dirs["app"], "main.py"), "w", encoding="utf-8") as f:
        f.write(main_code)

    # Save generated code to state
    state["generated_code"] = generated_code

    return state
