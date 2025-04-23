import uuid

def assign_id() -> str:
    print("[TransformFunctions:AssignID] Generating ID.")
    return str(uuid.uuid4())