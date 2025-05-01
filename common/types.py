from typing import TypeVar, Callable, Union, Awaitable
from pydantic import BaseModel
from common.internal_data import InternalData
from common.context_schemas import RelatedFieldContext, ContextFlag

T_ID          = TypeVar("T_ID")
TEntity       = TypeVar("TEntity")
TCreateDTO    = TypeVar("TCreateDTO", bound=BaseModel)
TUpdateDTO    = TypeVar("TUpdateDTO", bound=BaseModel)
TReadDTO      = TypeVar("TReadDTO", bound=BaseModel)
TInternalData = TypeVar("TInternalData", bound=InternalData)
TContextType = TypeVar("TContextType", bound=dict)

TransformFn = Callable[[TInternalData], Union[TInternalData, Awaitable[TInternalData]]]

PASSIVE_DELETION_FLAG = "passive_deletion"
RELATION_SETTED_FLAG = "relation_setted"