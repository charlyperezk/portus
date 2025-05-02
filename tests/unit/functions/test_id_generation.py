# tests/unit/test_id_generation.py

import uuid
import pytest
from src.utils.functions.id_generation import add_id

def test_id_generation_returns_uuid_string():
    data = add_id(field="id")
    
    assert isinstance(data, dict)
    
    try:
        parsed = uuid.UUID(data['id'])
    except ValueError:
        pytest.fail(f"Generated ID is not a valid UUID: {data['id']}")
    
    assert str(parsed) == data['id']