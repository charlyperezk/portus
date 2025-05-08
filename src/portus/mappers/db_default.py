from dataclasses import asdict
from portus.mappers import DBMapper
from portus.common.types import TDBModel, TEntity

class DefaultDBMapper(DBMapper[TDBModel, TEntity]):
    """
    A default implementation of the DBMapper class.
    This class provides a basic implementation for converting between database models and entities.
    """
    def to_model(self, entity: TEntity) -> TDBModel:
        """
        Convert an entity to a database model.
        """
        return self.model_cls(**asdict(entity))  # Assuming the model has a dict() method

    def from_model(self, model: TDBModel) -> TEntity:
        """
        Convert a database model to an entity.
        """
        return self.entity_cls(**model.to_dict())  # Assuming the entity has a dict() method
    
    def get_table_name(self) -> str:
        """
        Get the table name for the database model.
        """
        return self.model_cls.__tablename__