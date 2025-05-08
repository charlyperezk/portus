from portus.common.types import T_ID, TEntity
from portus.ports.output.repository import GetAndAskRepository, CrudRepository

class InMemoryStorage(GetAndAskRepository[T_ID, TEntity]):
    def __init__(self):
        self._storage: dict[T_ID, TEntity] = {}

    async def get(self, id: T_ID) -> TEntity | None:
        obj = self._storage.get(id)
        return obj

    async def exists(self, id: T_ID) -> bool:
        return True if await self.get(id) else False

class InMemoryRepository(CrudRepository[TEntity, T_ID], InMemoryStorage[T_ID, TEntity]):
    async def save(self, entity: TEntity) -> TEntity:
        self._storage[entity.id] = entity
        return entity
    
    async def list_all(self) -> list[TEntity]:
        all_objects = list(self._storage.values())        
        return all_objects

    async def update(self, entity: TEntity) -> TEntity:
        if entity.id in self._storage:
            self._storage[entity.id] = entity
            return entity
        
    async def delete(self, entity_id: T_ID) -> None:
        if entity_id in self._storage:
            del self._storage[entity_id]

    async def assign_id(self) -> T_ID:
        if self._storage:
            return max(self._storage.keys()) + 1
        return 1