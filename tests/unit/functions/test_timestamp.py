import pytest
from datetime import datetime
from hooks.functions.timestamp import get_timestamp, get_update_time

def test_get_timestamp_returns_created_and_updated():
    result = get_timestamp()

    # result should be a dict with both keys
    assert isinstance(result, dict)
    assert "created_at" in result
    assert "updated_at" in result

    # both values should be datetime instances
    assert isinstance(result["created_at"], datetime)
    assert isinstance(result["updated_at"], datetime)

def test_get_update_time_returns_updated_only():
    result = get_update_time()

    # result should be a dict with only 'updated_at'
    assert isinstance(result, dict)
    assert "updated_at" in result
    assert isinstance(result["updated_at"], datetime)
