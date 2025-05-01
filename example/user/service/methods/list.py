from example.user.repositories import CountryRelationRepository
from hooks.relation.setter import make_relation_context_hook

def get_transformation_hooks(country_repository: CountryRelationRepository):
    return [
        make_relation_context_hook("country_id", country_repository),
    ]