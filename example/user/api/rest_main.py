from fastapi import FastAPI
from example.user.dtos import UserCreateDTO, UserReadDTO, UserUpdateDTO
from example.user.service import UserService
from src.adapters.input.rest_controller.config import get_metadata
from src.adapters.input.rest_controller import FastAPIRestController

metadata = get_metadata()

app = FastAPI(
    title=metadata["title"],
    description=metadata["description"],
    version=metadata["version"],
    terms_of_service=metadata.get("terms_of_service"),
    contact=metadata.get("contact"),
    license_info=metadata.get("license_info"),
    openapi_tags=metadata.get("openapi_tags"),
    docs_url=metadata.get("docs_url", "/docs"),
    redoc_url=metadata.get("redoc_url", "/redoc"),
    openapi_url=metadata.get("openapi_url", "/openapi.json")
)

user_controller = FastAPIRestController(
    app=app,
    service=UserService(),
    create_dto=UserCreateDTO,
    read_dto=UserReadDTO,
    update_dto=UserUpdateDTO
)
user_controller.register_routes("users")