from src.portus.hooks.relation.setter import relation_context_hook

def get_transformation_hooks(country_repository):
    return [
        relation_context_hook("country_id", country_repository),
    ]