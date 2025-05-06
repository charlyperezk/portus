from typing import Dict, Any, List, Optional

def get_metadata(tags: Optional[List[Dict[str, str]]]=[]) -> Dict[str, Any]:
    data = {
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
    }
    if tags: 
        data["openapi_tags"] = tags
    
    return data