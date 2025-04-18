from services.database import SessionLocal, CodeLog
from langgraph_workflow import traceable, CodeState

@traceable(name="PersistToDB")
def persist_to_db_node(state: CodeState) -> CodeState:
    db = SessionLocal()

    try:
        generated_code = state.get("generated_code", {}).get("raw", "")
        generated_tests = state.get("generated_tests", "")
        debug_logs = state.get("debug_logs", "")
        zip_path = state.get("zip_path", "")
        entity = state.get("project_name", "default_project")

        log_entry = CodeLog(
            entity=entity,
            code=generated_code,
            test=generated_tests,
            debug_log=debug_logs,
            zip_path=zip_path
        )

        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        state["db_id"] = log_entry.id
        state["persisted"] = True

        print(f"Saved log to DB with ID: {log_entry.id}")

    except Exception as e:
        db.rollback()
        state["persisted"] = False
        state["persist_error"] = str(e)

    finally:
        db.close()

    return state 