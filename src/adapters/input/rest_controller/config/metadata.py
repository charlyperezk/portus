from typing import Dict, Any

def get_metadata() -> Dict[str, Any]:
    return {
        "title": "FastAPI-Portus CRUD REST API",
        "description": "A simple CRUD REST API using FastAPI and Portus.",
        "version": "0.1.0v",
        "terms_of_service": "https://example.com/terms/",
        "contact": {
            "name": "Carlos Pérez Küper",
            "url": "https://github.com/charlyperezk",
            "email": "carlosperezkuper@gmail.com",
        },
        "license_info": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT",
        },
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "openapi_url": "/openapi.json",
        "openapi_tags": [
            {
                "name": "users",
                "description": "Operations with users",
            },
            {
                "name": "countries",
                "description": "Operations with countries",
            },
        ]
    }
