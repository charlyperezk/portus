from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import Response
from typing import Generic, Type, Optional, List, Union
from portus.ports.input.crud import CRUDPort
from portus.common.logger import Logger, create_logger
from portus.common.types import T_ID, TCreateDTO, TReadDTO, TUpdateDTO

class FastAPIRestController(Generic[TCreateDTO, TReadDTO, TUpdateDTO]):
    def __init__(
        self,
        app: Union[FastAPI, APIRouter],
        service: CRUDPort[TCreateDTO, TReadDTO, TUpdateDTO, T_ID],
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

        @self.app.post(endpoint, response_model=self.read_dto, tags=[prefix])
        async def create(dto: self.create_dto): # type: ignore
            self.logger.info(f"Creating entity at {endpoint}")
            try:
                return await self.service.create(dto)
            except Exception as e:
                self.logger.error(f"There was an error creating entity - Detail: {e}")
                raise HTTPException(status_code=404, detail=str(e))

        @self.app.get(f"{endpoint}/{{entity_id}}", response_model=self.read_dto, tags=[prefix])
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

        @self.app.get(endpoint, response_model=List[self.read_dto], tags=[prefix])
        async def list_all():
            self.logger.info(f"Listing all entities at {endpoint}")
            try:
                return await self.service.list_all()
            except Exception as e:
                self.logger.error(f"There was an error listing entities - Detail: {e}")
                raise HTTPException(status_code=404, detail=str(e))

        if self.update_dto:
            @self.app.put(f"{endpoint}/{{entity_id}}", response_model=self.read_dto, tags=[prefix])
            async def update(entity_id: T_ID, dto: self.update_dto): # type: ignore
                self.logger.info(f"Updating entity {entity_id}")
                try:
                    return await self.service.update(entity_id, dto)
                except Exception as e:
                    self.logger.error(f"There was an error updating entity - Detail: {e}")
                    raise HTTPException(status_code=404, detail=str(e))

        @self.app.delete(f"{endpoint}/{{entity_id}}", tags=[prefix], response_class=Response)
        async def delete(entity_id: T_ID):
            self.logger.info(f"Deleting entity {entity_id}")
            try:
                if await self.service.delete(entity_id):
                    return Response(status_code=204)
                else:
                    self.logger.error(f"Entity not found - Detail: {e}")
                    raise HTTPException(status_code=404, detail="Entity not found")
            except Exception as e:
                self.logger.error(f"There was an error deleting entity - Detail: {e}")
                raise HTTPException(status_code=404, detail=str(e))
            
def set_controller(
        app: Union[FastAPI, APIRouter],
        service: CRUDPort,
        create_dto: Type[TCreateDTO],
        read_dto: Type[TReadDTO],
        update_dto: Optional[Type[TUpdateDTO]] = None        
) -> FastAPIRestController:
    controller = FastAPIRestController(
        app=app,
        service=service,
        create_dto=create_dto,
        read_dto=read_dto,
        update_dto=update_dto
    )
    return controller