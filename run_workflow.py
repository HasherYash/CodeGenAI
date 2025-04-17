from langgraph_workflow import build_langgraph

workflow = build_langgraph()

inputs = {

    "srs_path": "./sample_srs.docx"

}

final_state = workflow.invoke(inputs)

print("\n===== Generated Code =====\n")
print(final_state["generated_code"]["raw"])
print("\n===== Generated Tests =====\n")
print(final_state["generated_tests"])
print("\n===== Test Results =====\n")
print(final_state["test_results"])
if final_state.get("debug_logs"):
   print("\n===== Debug Logs / Fixes Applied =====\n")
   print(final_state["debug_logs"])