from common.types import T_ID, TEntity, T_Related_Id
from ports.output.repository import CrudRepository

class InMemoryRep(CrudRepository[TEntity, T_ID]):
    def __init__(self):
        self._storage: dict[T_ID, TEntity] = {}

    def save(self, entity: TEntity) -> TEntity:
        self._storage[entity.id] = entity
        return entity

    def get(self, entity_id: T_ID) -> TEntity | None:
        obj = self._storage.get(entity_id)
        return obj
    
    def list_all(self) -> list[TEntity]:
        all_objects = list(self._storage.values())        
        return all_objects

    def delete(self, entity_id: T_ID) -> None:
        if entity_id in self._storage:
            del self._storage[entity_id]

    def assign_id(self) -> T_ID:
        if self._storage:
            return max(self._storage.keys()) + 1
        return 1