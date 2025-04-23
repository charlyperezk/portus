from ports.output.repository import RelationRepository
from core.types import TInternalData
from hooks.base.hook import Hook

class RelationExistsHook(Hook):
    def __init__(self, repo: RelationRepository, field: str):
        self.repo = repo
        self.field = field

    def __call__(self, data: TInternalData) -> None:
        id_ = data[self.field]
        if not self.repo.exists(id_):
            raise ValueError(f"ID {id_} not found in relation.")