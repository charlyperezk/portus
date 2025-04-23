from dataclasses import dataclass

@dataclass(frozen=True)
class Country:
    id: str
    name: str