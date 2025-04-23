from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UserCreateDTO(BaseModel):
    username: str
    password: str
    email: str
    country_id: int

class UserUpdateDTO(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    country_id: Optional[int] = None

class UserReadDTO(BaseModel):
    id: str
    username: str
    created_at: datetime
    email: str
    country_id: int