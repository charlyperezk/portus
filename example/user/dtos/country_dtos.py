from pydantic import BaseModel

class CountryReadDTO(BaseModel):
    id: str
    name: str