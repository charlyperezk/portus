from typing import Callable, Any
from core.types import TInternalData
from hooks.base.hook import Hook

class ComputedFieldsHook(Hook):
    """
    Hook que ejecuta una función sin argumentos y fusiona su resultado con el InternalData.
    Ideal para campos calculados como timestamps, identificadores, etc.
    """
    def __init__(self, compute_fn: Callable[[], dict[str, Any]]):
        self._compute_fn = compute_fn

    def __call__(self, data: TInternalData) -> TInternalData:
        return data.merge(self._compute_fn())