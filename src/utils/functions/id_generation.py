import uuid

def add_id(field: str) -> str:
    return {
        field: str(uuid.uuid4())
    }