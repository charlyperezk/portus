from common.types import T_ID, TEntity
from adapters.output.in_memory import InMemoryStorage

class RelatedRepositoryInMemory(InMemoryStorage[T_ID, TEntity]):
    ...