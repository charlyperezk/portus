from example.user.entities import Country
from src.adapters.output.in_memory import RelatedRepositoryInMemory

class CountryRelationRepository(RelatedRepositoryInMemory[Country, str]):
    def __init__(self):
        super().__init__()
        self._storage = {
            1: Country(id=1, name="Argentina"),
            2: Country(id=2, name="Brasil")
        }