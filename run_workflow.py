import os
from dotenv import load_dotenv
from langgraph_workflow import build_langgraph

load_dotenv()

def run_codegen_workflow(srs_path: str, output_dir: str):
   workflow = build_langgraph()
   final_state = workflow.invoke({"srs_path": srs_path})

   generated_code = final_state.get("generated_code", {}).get("raw", "")
   if not generated_code:
       raise ValueError("No code generated.")

   os.makedirs(output_dir, exist_ok=True)
   with open(os.path.join(output_dir, "main.py"), "w") as f:
       f.write(generated_code)
