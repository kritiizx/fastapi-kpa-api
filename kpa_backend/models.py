# kpa_backend/models.py
from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users" # Name of the table in the database

    id = Column(Integer, primary_key=True, index=True) # Primary key, auto-incrementing
    phone = Column(String, unique=True, index=True, nullable=False) # Phone number, must be unique
    password_hash = Column(String, nullable=False) # Hashed password
    name = Column(String, nullable=True) # User's name
    email = Column(String, unique=True, nullable=True) # User's email, must be unique

    def __repr__(self):
        return f"<User(id={self.id}, phone='{self.phone}', name='{self.name}')>"