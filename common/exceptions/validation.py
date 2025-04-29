class ValidationError(Exception):
    @classmethod
    def field_not_found(cls, field: str):
        raise cls(f"Related field {field} not found")

    @classmethod
    def related_id_not_exists(cls, field, id):
        raise cls(f"{field} with value ({id}) not found in relationed repository.")