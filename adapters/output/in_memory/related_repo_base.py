from common.types import T_ID, TEntity, T_Related_Id
from ports.output.repository import RelationRepository

class RelatedRepositoryInMemory(RelationRepository[dict, T_Related_Id]):
    def __init__(self):
        self._storage: dict[T_ID, TEntity] = {}
    
    def get(self, entity_id: T_ID) -> TEntity | None:
        obj = self._storage.get(entity_id)
        return obj
    
    def exists(self, id):
        return True if self.get(id) else False