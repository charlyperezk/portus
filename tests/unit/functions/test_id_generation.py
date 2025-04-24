# tests/unit/test_id_generation.py

import uuid
import pytest
from common_utils.hooks.functions.id_generation import assign_id

def test_id_generation_returns_uuid_string():
    generated_id = assign_id()
    
    assert isinstance(generated_id, str)
    
    try:
        parsed = uuid.UUID(generated_id)
    except ValueError:
        pytest.fail(f"Generated ID is not a valid UUID: {generated_id}")
    
    assert str(parsed) == generated_id