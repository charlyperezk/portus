from portus.common.types import T_ID, TEntity
from portus.adapters.output.in_memory import InMemoryStorage

class RelatedRepositoryInMemory(InMemoryStorage[T_ID, TEntity]):
    ...