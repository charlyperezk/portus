import asyncio
from typing import List
from hooks.base import BaseHook
from common.types import TInternalData

class HookOrchestrator:
    def __init__(self):
        self.hooks: List[BaseHook] = []

    def add_hook(self, hook: BaseHook) -> "HookOrchestrator":
        self.hooks.append(hook)
        return self

    async def _maybe_await(self, result):
        if asyncio.iscoroutine(result):
            return await result
        return result

    async def run(self, data: TInternalData) -> TInternalData:
        current_data = data
        for hook in self.hooks:
            result = await self._maybe_await(hook(current_data))
            current_data = result
        return current_data

    @classmethod
    def from_hooks(cls, hooks: List[BaseHook]) -> "HookOrchestrator":
        orchestrator = cls()
        for hook in hooks:
            orchestrator.add_hook(hook)
        return orchestrator
