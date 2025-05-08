from pydantic import BaseModel
from beanie import Document
from typing import TypeVar, Callable, Union, Awaitable
from sqlalchemy.orm import DeclarativeBase
from portus.common.internal_data import InternalData
from portus.common.context_schemas import RelatedFieldContext, ContextFlag


T_ID          = TypeVar("T_ID", bound=Union[int, str])
TEntity       = TypeVar("TEntity")
TCreateDTO    = TypeVar("TCreateDTO", bound=BaseModel)
TUpdateDTO    = TypeVar("TUpdateDTO", bound=BaseModel)
TReadDTO      = TypeVar("TReadDTO", bound=BaseModel)
TInternalData = TypeVar("TInternalData", bound=InternalData)
TDBModel = TypeVar("TDBModel", bound=Union[DeclarativeBase, Document])
TransformFn = Callable[[TInternalData], Union[TInternalData, Awaitable[TInternalData]]]

PASSIVE_DELETION_FLAG = "passive_deletion"
RELATION_SETTED_FLAG = "relation_setted"