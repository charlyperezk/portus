import datetime
from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    id: str
    username: str
    password_hash: str
    created_at: datetime
    updated_at: datetime
    role: str
    verified: bool
    active: bool
    email: str
    country_id: int