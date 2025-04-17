from langgraph_workflow import build_langgraph
workflow = build_langgraph()
# Provide your local SRS .docx path
inputs = {
   "srs_path": "./sample_srs.docx"
}
final_state = workflow.invoke(inputs)
print("\n===== Extracted Info =====\n")
print(final_state["extracted_info"]["raw"])