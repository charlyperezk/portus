from hooks.core.setters import RelationFieldAssignerHook
from common.internal_data import InternalData
from example.user.entities import Country

class RelatedCountryAssignerHook(RelationFieldAssignerHook):
    def set(self, data: InternalData, object: Country) -> InternalData:
        return data.merge({'country': object.name})