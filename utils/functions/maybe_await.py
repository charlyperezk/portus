import asyncio
from typing import Any
from common.types import TInternalData

async def maybe_await(result: TInternalData) -> TInternalData:
    if asyncio.iscoroutine(result):
        return await result
    return result