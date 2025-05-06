from datetime import datetime
from pydantic import BaseModel, Field

class CountryCreateDTO(BaseModel):
    name: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "ExampleCountry"
            }
        }

class CountryUpdateDTO(CountryCreateDTO):
    ...

class CountryReadDTO(BaseModel):
    id: int
    name: str
    # created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1",
                "username": "ExampleUser",
                # "created_at": "2025-10-01T12:00:00Z",
            }
        }