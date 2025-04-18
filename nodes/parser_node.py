import os
from typing import Dict
from docx import Document
from langchain_core.messages import HumanMessage
from langgraph_workflow import traceable, CodeState, llm

@traceable(name="ParseSRS")
def parse_srs_node(state: Dict) -> Dict:
    path = state.get("srs_path")

    if not path or not os.path.exists(path):
        raise ValueError("Missing or invalid SRS file path")

    # Step 1: Extract text from DOCX
    doc = Document(path)
    content = "\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())
    state["srs_content"] = content

    # Step 2: Construct prompt for LLM to extract requirements and structure
    prompt1 = f"""
    You are a senior backend software architect. Given the following Software Requirements Specification (SRS):

    {content}

    Extract the following:
    - Requirement of backend, database communication and Deployment related technologies to use
    - Required Users
    - API endpoints from Functionality with required API call and examples
    - Authentication and Authorization requirements with required API call and examples
    - Required models and their attributes
    - Create Database schema (tables, fields, types, relationships)
    """

    extracted_info = llm.invoke(prompt1).content

    prompt2 = f"""
    You are a senior backend software architect. Given the following extracted information from the SRS:

    {extracted_info}

    Propose a clean Python FastAPI project folder structure that supports modular backend development. Structure must include separate folders for:
    - app code (e.g., routes, models, schemas, services)
    - database config
    - test files
    - documentation
    - Docker/Podman-related files
    """

    # Step 4: Parse output sections
    project_structure_plan = llm.invoke(prompt2).content

    # Step 5: Store both in state
    state["extracted_info"] = extracted_info
    state["project_structure_plan"] = project_structure_plan

    return state
