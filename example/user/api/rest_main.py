from fastapi import FastAPI
from contextlib import asynccontextmanager
from example.user.api.router_setter import set_user_routes
from example.countries.api.router_setter import set_country_routes
from example.user.persistency.repositories.sqlalchemy.config import DATABASE_URL
from src.portus.adapters.output.sqlalchemy.base import Base, create_all_tables
from src.portus.adapters.input.rest_controller.config import get_metadata

tags=[
        {
            "name": "countries",
            "description": "Countries CRUD operations",
        },
        {
            "name": "users",
            "description": "Users CRUD operations",
        }
    ]

metadata = get_metadata(tags=tags)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables(DATABASE_URL)
    yield

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
    openapi_url=metadata.get("openapi_url", "/openapi.json"),
    lifespan=lifespan
)

user_controller = set_user_routes(app)
user_controller.register_routes("users")
user_controller = set_country_routes(router=app)
user_controller.register_routes("countries")