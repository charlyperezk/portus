from dataclasses import dataclass, asdict
from typing import Dict

@dataclass(frozen=True)
class UserCreateDefaultConfig:
    role: str = "standard"
    active: bool = True
    verified: bool = False

    def as_dict(self) -> Dict[str, bool]:
        return asdict(self)

user_defaults = UserCreateDefaultConfig().as_dict()