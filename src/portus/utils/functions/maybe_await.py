import asyncio
from portus.common.types import TInternalData

async def maybe_await(result: TInternalData) -> TInternalData:
    if asyncio.iscoroutine(result):
        return await result
    return result