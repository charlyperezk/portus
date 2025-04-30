from typing import TypeVar
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

PASSIVE_DELETION_FLAG = "passive_deletion"
RELATION_SETTED_FLAG = "relation_setted"