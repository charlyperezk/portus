from ports.output.repository import GetAndAskRepository
from common.types import TInternalData
from hooks.base.hook import Hook

class RelationExistsHook(Hook):
    def __init__(self, repo: GetAndAskRepository, field: str):
        self.repo = repo
        self.field = field

    def __call__(self, data: TInternalData) -> None:
        id_ = data.__getattr__(self.field)
        if not self.repo.exists(id_):
            raise ValueError(f"{self._field} with value ({id_}) not found in relationed repository.")