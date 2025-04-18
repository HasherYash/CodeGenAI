import os

def get_project_dirs(root: str):

    return {
        "root": root,
        "models": os.path.join(root, "app", "models"),
        "routers": os.path.join(root, "app", "routers"),
        "services": os.path.join(root, "app", "services"),
        "app": os.path.join(root, "app"),
    } 