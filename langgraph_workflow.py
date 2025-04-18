import os
import logging
import functools
from typing import TypedDict, Optional, Dict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.runnables import Runnable

# ===== Logging Setup =====
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== Traceable Decorator =====
def traceable(name: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Entering {name}")
            result = func(*args, **kwargs)
            logger.info(f"Exiting {name}")
            return result
        return wrapper
    return decorator

# ===== Environment Variables for LLM =====
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "FastAPI-Generator")
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# ===== Initialize Shared LLM =====

llm = ChatGroq(
    model_name="llama3-8b-8192",
    temperature=0.2,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# ===== Define Shared State Structure =====

class CodeState(TypedDict):
    srs_path: Optional[str]
    srs_content: Optional[str]
    extracted_info: Optional[Dict]
    project_dir: Optional[str]
    generated_code: Optional[Dict]
    generated_tests: Optional[str]
    test_results: Optional[str]
    debug_logs: Optional[str]
    zip_path: Optional[str]
    docs: Optional[Dict]
    project_structure: Optional[Dict]


# ===== Import Nodes =====

from nodes.parser_node import parse_srs_node
from nodes.project_structure import prepare_project_structure_node
from nodes.code_gen_node import codegen_node
from nodes.test_gen_node import testgen_node
from nodes.execute_and_debug_node import execute_and_debug_node
from nodes.generate_docs_node import generate_docs_node
from nodes.persist_to_db_node import persist_to_db_node
from nodes.zip_node import zip_node

# ===== Build LangGraph =====

def build_langgraph() -> Runnable:

    builder = StateGraph(CodeState)

    # Register nodes
    builder.add_node("ParseSRS", parse_srs_node)
    builder.add_node("PrepareProject", prepare_project_structure_node)
    builder.add_node("CodeGen", codegen_node)
    builder.add_node("TestGen", testgen_node)
    builder.add_node("ExecuteDebug", execute_and_debug_node)
    builder.add_node("GenerateDocs", generate_docs_node)
    builder.add_node("Persist", persist_to_db_node)
    builder.add_node("ZipProject", zip_node)

    # Define execution order

    builder.set_entry_point("ParseSRS")
    builder.add_edge("ParseSRS", "PrepareProject")
    builder.add_edge("PrepareProject", "CodeGen")
    builder.add_edge("CodeGen", "TestGen")
    builder.add_edge("TestGen", "ExecuteDebug")
    builder.add_conditional_edges(
        "ExecuteDebug",
        lambda state: "Fixing" if state.get("test_results") and "FAILED" in state["test_results"] else "Done",
        {
            "Fixing": "CodeGen",
            "Done": "GenerateDocs"
        }
    )

    builder.add_edge("GenerateDocs", "Persist")
    builder.add_edge("Persist", "ZipProject")
    builder.add_edge("ZipProject", END)
    return builder.compile()

# ===== Exports for Other Node Files =====
__all__ = ["llm", "traceable", "CodeState"] 