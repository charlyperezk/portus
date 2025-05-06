import datetime
from typing import Optional
from dataclasses import dataclass

@dataclass(frozen=True)
class Country:
    name: str
    id: Optional[str] = None
    # created_at: datetime
    # updated_at: datetime