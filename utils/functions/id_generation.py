import uuid

def add_id(field: str) -> str:
    return {
        'id': str(uuid.uuid4())
    }