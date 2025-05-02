from fastapi import FastAPI, HTTPException
from typing import Generic, Type, Optional
from src.core.services.crud import CRUDService
from src.common.logger import Logger, create_logger
from src.common.types import T_ID, TEntity, TCreateDTO, TReadDTO, TUpdateDTO, TInternalData

class FastAPIRestController(Generic[TCreateDTO, TReadDTO, TUpdateDTO]):
    def __init__(
        self,
        app: FastAPI,
        service: CRUDService[T_ID, TEntity, TCreateDTO, TReadDTO, TInternalData, TUpdateDTO],
        create_dto: Type[TCreateDTO],
        read_dto: Type[TReadDTO],
        update_dto: Optional[Type[TUpdateDTO]] = None,
        logger: Optional[Logger] = None
    ):
        self.app = app
        self.service = service
        self.create_dto = create_dto
        self.read_dto = read_dto
        self.update_dto = update_dto
        logger_name = f"{self.__class__.__name__}:{self.service.__class__.__name__}"
        self.logger = logger or create_logger(logger_name)
    
    def register_routes(self, prefix: str = ""):
        endpoint = f"/{prefix}" if prefix else ""

        @self.app.post(endpoint, response_model=Optional[self.read_dto], tags=[prefix])
        async def create(dto: self.create_dto): # type: ignore
            self.logger.info(f"Creating entity at {endpoint}")
            try:
                return await self.service.create(dto)
            except Exception as e:
                self.logger.error(f"There was an error creating entity - Detail: {e}")
                raise HTTPException(status_code=404, detail=str(e))

        @self.app.get(f"{endpoint}/{{entity_id}}", response_model=Optional[self.read_dto], tags=[prefix])
        async def read(entity_id: T_ID):
            self.logger.info(f"Reading entity {entity_id}")
            try:
                result = await self.service.get(entity_id)
                if not result:
                    self.logger.error(f"Entity not found - Trace: {e}")
                    raise HTTPException(status_code=404, detail="Entity not found")
            except Exception as e:
                self.logger.error(f"There was an error reading entity - Detail: {e}")
                raise HTTPException(status_code=404, detail=str(e))
            return result


        if self.update_dto:
            @self.app.put(f"{endpoint}/{{entity_id}}", response_model=Optional[self.read_dto], tags=[prefix])
            async def update(entity_id: T_ID, dto: self.update_dto): # type: ignore
                self.logger.info(f"Updating entity {entity_id}")
                try:
                    return await self.service.update(entity_id, dto)
                except Exception as e:
                    self.logger.error(f"There was an error updating entity - Detail: {e}")
                    raise HTTPException(status_code=404, detail=str(e))

        @self.app.delete(f"{endpoint}/{{entity_id}}", tags=[prefix])
        async def delete(entity_id: T_ID):
            self.logger.info(f"Deleting entity {entity_id}")
            try:
                return await self.service.delete(entity_id)
            except Exception as e:
                self.logger.error(f"There was an error deleting entity - Detail: {e}")
                raise HTTPException(status_code=404, detail=str(e))