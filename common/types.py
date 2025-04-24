from typing import TypeVar, Dict, Any
from pydantic import BaseModel
from common.internal_data import InternalData

T_ID          = TypeVar("T_ID")
TEntity       = TypeVar("TEntity")
TCreateDTO    = TypeVar("TCreateDTO", bound=BaseModel)
TUpdateDTO    = TypeVar("TUpdateDTO", bound=BaseModel)
TReadDTO      = TypeVar("TReadDTO", bound=BaseModel)
TInternalData = TypeVar("TInternalData", bound=InternalData)