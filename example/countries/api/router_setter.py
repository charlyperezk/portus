from fastapi import APIRouter
from example.countries.dtos import CountryCreateDTO, CountryReadDTO, CountryUpdateDTO
from example.countries.service import CountryService
from src.adapters.input.rest_controller import set_controller

def set_country_routes(router: APIRouter):
    return set_controller(
        router,
        CountryService(),
        CountryCreateDTO,
        CountryReadDTO, 
        CountryUpdateDTO
    )