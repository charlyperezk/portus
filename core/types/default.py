from uuid import UUID
from pydantic import BaseModel
from typing import TypeVar
from core.types.internal_data import InternalData

Hashed_ID = type[UUID]
T_ID = TypeVar("TId", bound=[int, str, Hashed_ID])
TEntity = TypeVar("TEntity")
TCreateDTO = TypeVar("TCreateDTO", bound=BaseModel)
TUpdateDTO = TypeVar("TUpdateDTO", bound=BaseModel)
TReadDTO = TypeVar("TReadDTO", bound=BaseModel)
T_Related_Id = TypeVar("T_Related_Id", bound=[int, str])

TInternalData = TypeVar("TInternalData", bound=InternalData)