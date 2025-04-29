from hooks.base import BaseHook
from common.types import TInternalData
from typing import Callable
from logging import Logger

class LogCompositorHook(BaseHook):
    def __init__(
        self,
        logger: Logger,
        log_composition_fn: Callable[[TInternalData], str]
    ):
        self.logger = logger
        self.log_composition_fn = log_composition_fn

    async def __call__(self, data: TInternalData) -> TInternalData:
        message = self.log_composition_fn(data)
        self.logger.info(message)
        return data