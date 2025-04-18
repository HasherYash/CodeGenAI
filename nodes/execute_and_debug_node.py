import os
import subprocess
import tempfile
import traceback
from langgraph_workflow import traceable, CodeState, llm

@traceable(name="ExecuteDebug")
def execute_and_debug_node(state: CodeState) -> CodeState:
    code = state["generated_code"]
    tests = state["generated_tests"]

    with tempfile.TemporaryDirectory() as tmp:

        # Step 1: Create structured directory
        project_dir = os.path.join(tmp, "project")
        os.makedirs(project_dir, exist_ok=True)
        main_file = os.path.join(project_dir, "main.py")
        test_file = os.path.join(project_dir, "test_main.py")

        with open(main_file, "w") as f:
            f.write("code")

        with open(test_file, "w") as f:
            f.write("tests")

        try:
            # Step 2: Run pytest on test file
            result = subprocess.run(
                ["pytest", "--tb=short", test_file],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=30
            )

            state["test_results"] = result.stdout + "\n" + result.stderr
            if result.returncode != 0:

                # Step 3: If test failed, loop back to CodeGen with fix prompt
                fix_prompt = f"""Fix this FastAPI code so it passes the following tests.
                Code:{code}
                Tests:{tests}
                Errors:{state['test_results']}
                """

                # Use the same LLM instance from earlier
                fix = llm.invoke(fix_prompt)
                state["generated_code"]["raw"] = fix.content
                state["debug_logs"] = state["test_results"]
                state["fix_required"] = True

            else:
                state["fix_required"] = False  # All tests passed

        except Exception:
            state["test_results"] = "Execution error."
            state["debug_logs"] = traceback.format_exc()
            state["fix_required"] = True

    return state 