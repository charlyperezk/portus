from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserCreateDTO(BaseModel):
    username: str
    password: str
    email: EmailStr
    country_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "username": "ExampleUser",
                "password": "PasswordString",
                "email": "example@gmail.com",
                "country_id": 1
            }
        }

class UserUpdateDTO(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    country_id: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "username": "ExampleUser",
                "email": "example@gmail.com",
                "country_id": None
            }
        }

class UserReadDTO(BaseModel):
    id: str
    username: str
    created_at: datetime
    email: str
    country: dict

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1",
                "username": "ExampleUser",
                "created_at": "2023-10-01T12:00:00Z",
                "email": "example@gmail.com",
                "country": {
                    "id": 1,
                    "name": "ExampleCountry"
                }
            }
        }