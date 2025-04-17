import os
from typing import TypedDict, Optional
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langchain_core.runnables import Runnable
from docx import Document
# ==== Step 1: Define State ====
class CodeState(TypedDict):
   srs_path: Optional[str]
   srs_content: Optional[str]
   extracted_info: Optional[dict]
   generated_code: Optional[dict]

# ==== Step 2: Helper Function to Extract Text ====
def extract_text_from_docx(file_path: str) -> str:
   doc = Document(file_path)
   return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

# ==== Step 3: Setup LLM (Groq) ====
llm = ChatGroq(
   groq_api_key=os.getenv("GROQ_API_KEY"),  # safer; or use string here directly for testing
   model_name="llama3-70b-8192"
)

# ==== Step 4: Define LangGraph Nodes ====
# Node 1: Parse the SRS file and extract info
def parse_srs_node(state: CodeState) -> CodeState:
   print("[Parser Node] Reading .docx and extracting structured data...")
   srs_path = state.get("srs_path")
   if not srs_path or not os.path.exists(srs_path):
       raise FileNotFoundError("SRS .docx file not found!")
   srs_text = extract_text_from_docx(srs_path)
   state["srs_content"] = srs_text
   prompt = f"""
You are a backend architect. Analyze the following SRS content and extract:
1. List of API endpoints with HTTP methods and parameters
2. Database schema (tables, fields, types, relationships)
3. Required models and attributes
4. Authentication & Authorization requirements
SRS Document:
{srs_text}
   """
   print("[LLM] Sending prompt to Groq (LLaMA3)...")
   response = llm.invoke(prompt)
   state["extracted_info"] = {"raw": response.content}
   return state

# ==== Step 5: Build LangGraph ====
def build_langgraph() -> Runnable:
   builder = StateGraph(CodeState)
   builder.add_node("ParseSRS", parse_srs_node)
   builder.set_entry_point("ParseSRS")
   builder.add_edge("ParseSRS", END)
   return builder.compile()