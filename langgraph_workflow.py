import os

import subprocess

import tempfile

import traceback

from typing import TypedDict, Optional

from docx import Document

from langgraph.graph import StateGraph, END

from langchain_core.runnables import Runnable

from langchain_groq import ChatGroq

# === Initialize LLM ===

llm = ChatGroq(

    model_name="llama3-8b-8192",

    temperature=0.2,

    groq_api_key=os.getenv("GROQ_API_KEY")

)

# === Shared State ===

class CodeState(TypedDict):

    srs_path: Optional[str]

    srs_content: Optional[str]

    extracted_info: Optional[dict]

    generated_code: Optional[dict]

    generated_tests: Optional[str]  # <- NEW

    test_results: Optional[str]

    debug_logs: Optional[str]


# === Parser Node ===

def parse_srs_node(state: CodeState) -> CodeState:

    print("[ParseSRS] Extracting content from SRS document...")

    path = state.get("srs_path")

    if not path:

        raise ValueError("Missing SRS path")

    doc = Document(path)

    content = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

    state["srs_content"] = content

    state["extracted_info"] = {

        "raw": f"Mock Extracted Functional Requirements:\n{content[:500]}"

    }

    return state


# === CodeGen Node ===

def codegen_node(state: CodeState) -> CodeState:

    print("[CodeGen] Generating FastAPI backend code...")

    extracted = state.get("extracted_info", {}).get("raw", "")

    if not extracted:

        raise ValueError("No extracted info found for code generation!")

    prompt = f"""

You are a senior FastAPI engineer.

Generate Python backend code based on the following software requirements:

{extracted}

Include:

1. Pydantic models (User, Item)

2. API routes (/users, /items)

3. Services (logic)

4. main.py

5. Logging & error handling

Use clean modular structure and include comments.

    """

    response = llm.invoke(prompt)

    state["generated_code"] = {"raw": response.content}

    return state


# === TestGen Node ===

def testgen_node(state: CodeState) -> CodeState:

    print("[TestGen] Generating unit tests using pytest...")

    code = state.get("generated_code", {}).get("raw", "")

    if not code:

        raise ValueError("Code not available for testing")

    prompt = f"""

You are a Python test engineer.

Write pytest-based unit tests for the following FastAPI backend code.

Include:

- Route tests

- Model tests

- Service tests

- Edge cases

Code:

{code}

    """

    response = llm.invoke(prompt)

    state["generated_tests"] = response.content

    return state

# === Code Execution and Debug Log Node ===

def execute_and_debug_node(state: CodeState) -> CodeState:
   print("[Execution] Running generated code and unit tests...")
   code = state.get("generated_code", {}).get("raw", "")
   tests = state.get("generated_tests", "")
   with tempfile.TemporaryDirectory() as temp_dir:
       main_path = os.path.join(temp_dir, "main.py")
       test_path = os.path.join(temp_dir, "test_main.py")
       with open(main_path, "w", encoding="utf-8") as f:
           f.write(code)
       with open(test_path, "w", encoding="utf-8") as f:
           f.write(tests)
       # Run pytest
       try:
           result = subprocess.run(
               ["pytest", "--tb=short", test_path],
               cwd=temp_dir,
               capture_output=True,
               text=True,
               timeout=30
           )
           passed = result.returncode == 0
           output = result.stdout + "\n" + result.stderr
           state["test_results"] = output
           if not passed:
               print("[Debugging] Tests failed. Invoking LLM for fix...")
               # Ask LLM to fix the code based on the test output
               fix_prompt = f"""
You wrote this code:
{code}
And these were the tests:
{tests}
The following test output indicates errors:
{output}
Please fix the code and provide an updated version of main.py that passes all tests.
"""
               fix_response = llm.invoke(fix_prompt)
               state["generated_code"]["raw"] = fix_response.content
               state["debug_logs"] = output
           else:
               print("[Execution] All tests passed.")
       except Exception as e:
           state["test_results"] = "Execution error."
           state["debug_logs"] = traceback.format_exc()
   return state


# === Build LangGraph Workflow ===

def build_langgraph() -> Runnable:

    builder = StateGraph(CodeState)

    builder.add_node("ParseSRS", parse_srs_node)

    builder.add_node("CodeGen", codegen_node)

    builder.add_node("TestGen", testgen_node)

    builder.add_node("ExecuteDebug", execute_and_debug_node)  # NEW

    builder.set_entry_point("ParseSRS")

    builder.add_edge("ParseSRS", "CodeGen")

    builder.add_edge("CodeGen", "TestGen")

    builder.add_edge("TestGen", "ExecuteDebug")

    builder.add_edge("ExecuteDebug", END)

    return builder.compile() 