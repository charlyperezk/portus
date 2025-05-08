from typing import Optional, Sequence, Type
from beanie import init_beanie, Document
from motor.motor_asyncio import AsyncIOMotorClient
from portus.common.logger import Logger, create_logger

class BeanieAsyncAdapter:
    def __init__(
        self,
        db_url: str,
        db_name: str,
        document_models: Sequence[Type[Document]],
        logger: Optional[Logger] = None,
    ):
        self.db_url = db_url
        self.db_name = db_name
        self.client = AsyncIOMotorClient(self.db_url)
        self.database = self.client[self.db_name]
        self.document_models = document_models
        self.logger = logger or create_logger("BeanieAsyncAdapter")

    async def init(self):
        self.logger.debug(f"Initializing Beanie with database '{self.db_name}'")
        await init_beanie(database=self.database, document_models=self.document_models)
        self.logger.info("Beanie initialization completed")

    async def close(self):
        self.logger.debug("Closing MongoDB client connection")
        self.client.close()

    def get_model(self, model_cls: Type[Document]) -> Type[Document]:
        if model_cls not in self.document_models:
            raise ValueError(f"{model_cls.__name__} is not a registered document model.")
        return model_cls

