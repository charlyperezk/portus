from ports.output.repository import RelationRepository
from common.types import TInternalData
from hooks.base.hook import Hook

class RelationFieldAssignerHook(Hook):
    def __init__(self, repo: RelationRepository, field: str):
        self.repo = repo
        self.field = field

    def __call__(self, data: TInternalData) -> None:
        id_ = data.__getattr__(self.field)
        related_object = self.repo.get(id_)
        return self.set(data, related_object)

    def set(self, data: TInternalData, object) -> TInternalData:
        raise NotImplementedError("You must implement the set method.")