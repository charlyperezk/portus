from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreateDTO(BaseModel):
    username: str
    password: str
    email: EmailStr
    country_id: int

class UserUpdateDTO(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    country_id: Optional[int] = None

class UserReadDTO(BaseModel):
    id: str
    username: str
    created_at: datetime
    email: str
    country: dict