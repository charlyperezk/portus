from src.hooks.base import BaseHook
from src.common.types import TInternalData, TransformFn
from src.common.exceptions import TransformationError

class DataTransformerHook(BaseHook):
    def __init__(self, transform_fn: TransformFn):
        self.transform_fn = transform_fn

    async def __call__(self, data: TInternalData) -> TInternalData:
        try:
            result = self.transform_fn(data)
            return await self._maybe_await(result)
        except Exception as e:
            raise TransformationError(e)