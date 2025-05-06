from fastapi import APIRouter
from example.countries.dtos import CountryCreateDTO, CountryReadDTO, CountryUpdateDTO
from example.countries.service import CountryService
from src.adapters.input.rest_controller import FastAPIRestController

def set_country_routes(router: APIRouter):
    return FastAPIRestController(
        app=router,
        service=CountryService(),
        create_dto=CountryCreateDTO,
        read_dto=CountryReadDTO,
        update_dto=CountryUpdateDTO
    )