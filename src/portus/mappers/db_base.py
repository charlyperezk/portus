from abc import ABC, abstractmethod
from portus.common.types import TDBModel, TEntity
from typing import Generic, Type

class DBMapper(Generic[TDBModel, TEntity], ABC):
    """
    A generic mapper class for converting between database models and dictionaries.
    """
    def __init__(self, model_cls: Type[TDBModel], entity_cls: Type[TEntity]):
        self.model_cls = model_cls
        self.entity_cls = entity_cls  # Assuming the model has an entity class attribute

    @abstractmethod
    def to_model(self, entity: TEntity) -> TDBModel:
        ...

    @abstractmethod
    def from_model(self, model: TDBModel) -> TEntity:
        ...

    @abstractmethod
    def get_table_name(self) -> str:
        ...

    def get_model_class(self) -> Type[TDBModel]:
        return self.model_cls