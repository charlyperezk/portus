from fastapi import FastAPI
from example.countries.api.router_setter import set_country_routes
from src.portus.adapters.input.rest_controller.config import get_metadata

tags=[
        {
            "name": "countries",
            "description": "Countries CRUD operations",
        }
    ]

metadata = get_metadata(tags=tags)

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

# country_controller = set_country_routes(router=app)
# country_controller.register_routes("countries")