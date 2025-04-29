import pytest
from utils.functions.security import hash_password, verify_password

def test_password_hash_returns_valid_hash():
    raw = "SuperSecret123!"
    hashed = hash_password(raw)

    assert isinstance(hashed, str)
    assert hashed != raw

    assert verify_password(raw, hashed)