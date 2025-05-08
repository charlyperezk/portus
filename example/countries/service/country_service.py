from src.portus.mappers.default import DefaultMapper
from src.portus.common.types import InternalData
from src.portus.core.services import CRUDService

from example.countries.dtos import CountryCreateDTO, CountryReadDTO, CountryUpdateDTO
from example.countries.entities import Country
from example.countries.config.loggers import service_logger
from example.countries.persistency import CountryRepository

class CountryService(
    CRUDService[int, Country, CountryCreateDTO, CountryReadDTO, InternalData, CountryUpdateDTO]
):
    def __init__(self):
        super().__init__(
            repository=CountryRepository(), # Replace with actual repository
            mapper=DefaultMapper(Country, CountryReadDTO, InternalData),
            logger=service_logger,
            related_repositories={},
        )

    ...