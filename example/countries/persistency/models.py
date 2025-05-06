from datetime import datetime
from src.adapters.output.sqlalchemy.base import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

class CountryDBModel(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)

    # users = relationship("User", back_populates="country")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
    
    def __repr__(self):
        return f"CountryDBModel(id={self.id}, name={self.name})"