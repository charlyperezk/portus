from datetime import datetime
from example.countries.persistency.models import CountryDBModel
from src.portus.adapters.output.sqlalchemy.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class UserDBModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    email = Column(String, unique=True, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    role = Column(String, default="user")
    verified = Column(String, default="false")
    active = Column(String, default="true")

    # country = relationship("Country", back_populates="users")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password_hash": self.password_hash,
            "email": self.email,
            "country_id": self.country_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "role": self.role,
            "verified": self.verified,
            "active": self.active
        }
    
    def __repr__(self):
        return f"UserDBModel(id={self.id}, username={self.username}, email={self.email}, country_id={self.country_id})"