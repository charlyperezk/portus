class ValidationError(Exception):
    @classmethod
    def field_not_found(cls, field: str):
        return cls(f"Related field {field} not found")

    @classmethod
    def related_id_not_exists(cls, field, id):
        return cls(f"{field} with value ({id}) not found in related repository.")
    
    @classmethod
    def id_not_exists(cls, id):
        return cls(f"Entity with ID {id} not found.")