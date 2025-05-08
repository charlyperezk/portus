class RepositoryException(Exception):
    """Base class for all repository exceptions."""
    pass

class EntityNotFoundException(RepositoryException):
    """Exception raised when an entity is not found in the repository."""
    def __init__(self, entity_id: str):
        super().__init__(f"Entity with ID {entity_id} not found.")
        self.entity_id = entity_id

class EntityAlreadyExistsException(RepositoryException):
    """Exception raised when an entity already exists in the repository."""
    def __init__(self, entity_id: str):
        super().__init__(f"Entity with ID {entity_id} already exists.")
        self.entity_id = entity_id

class EntityNotActiveException(RepositoryException):
    """Exception raised when an entity is not active in the repository."""
    def __init__(self, entity_id: str):
        super().__init__(f"Entity with ID {entity_id} is not active.")
        self.entity_id = entity_id    