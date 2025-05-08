import time
from logging import Logger
from typing import List, Optional
from portus.hooks.base import BaseHook
from portus.common.logger import create_logger
from portus.common.types import TInternalData
from portus.utils.functions import maybe_await

class HookOrchestrator:
    def __init__(self, logger: Logger=None):
        self.hooks: List[BaseHook] = []
        self.logger = logger or create_logger("HookOrchestrator")

    def add_hook(self, hook: BaseHook) -> "HookOrchestrator":
        self.hooks.append(hook)
        return self

    async def run(self, data: TInternalData, process_name: Optional[str] = "process") -> TInternalData:
        hook_types = [hook.__class__.__name__ for hook in self.hooks]
        self.logger.debug(f"Executing {len(self.hooks)} {process_name} hooks: {hook_types}")

        current_data = data
        start_time = time.perf_counter()

        for i, hook in enumerate(self.hooks):
            result = await maybe_await(hook(current_data))
            if result is None:
                self.logger.warning(f"Hook ({i+1} of {len(self.hooks)}) returned None")
            current_data = result

        duration_ms = (time.perf_counter() - start_time) * 1000
        self.logger.debug(f"Execution finished successfully in {duration_ms:.2f}ms")

        return current_data

    @classmethod
    def from_hooks(cls, hooks: List[BaseHook], logger: Logger
                   ) -> "HookOrchestrator":
        _logger = logger or create_logger("HookOrchestrator")
        orchestrator = cls(logger=_logger)
        for hook in hooks:
            orchestrator.add_hook(hook)
        return orchestrator
