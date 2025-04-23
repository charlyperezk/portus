from typing import Optional, Literal
from core.types import TInternalData
from hooks.base.hook import CompositeHook

class ValidateAndTransformComposite:
    def __init__(self, validations: CompositeHook, transformations: CompositeHook):
        self.validations = validations
        self.transformations = transformations

    async def run_validations(self, data: TInternalData) -> Optional[TInternalData]:
        return await self.validations.run(data)
    
    async def run_transformations(self, data: TInternalData) -> TInternalData:
        return await self.transformations.run(data)
    
    async def __call__(self, data: TInternalData) -> TInternalData:
        await self.run_validations(data)
        return await self.run_transformations(data)

    @classmethod
    def from_hooks(cls, hooks: dict[Literal["validations", "transformations"],
                                     CompositeHook]) -> 'ValidateAndTransformComposite':
        return cls(**hooks)

class LifeCycle:
    def __init__(self, before: Optional[ValidateAndTransformComposite] = None,
                  after: Optional[CompositeHook] = None):
        self.before = before
        self.after = after

        assert (
            before is None or isinstance(before, ValidateAndTransformComposite)
        ), "Before must be an instance of ValidateAndTransformComposite or None"

        assert (
            after is None or isinstance(after, CompositeHook)
        ), "After must be an instance of CompositeHook or None"

    def has_before(self) -> bool:
        return self.before is not None

    def has_after(self) -> bool:
        return self.after is not None
        
    async def run_before_hooks(self, data: TInternalData) -> TInternalData:
        return await self.before(data)
    
    async def run_after_hooks(self, data: TInternalData) -> None:
        return await self.after(data)