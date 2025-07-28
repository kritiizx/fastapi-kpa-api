# kpa_backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create a SQLAlchemy engine
# The echo=True argument will print all SQL statements executed
engine = create_engine(DATABASE_URL, echo=True)

# Create a SessionLocal class
# This will be used to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models
Base = declarative_base()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create all tables defined in Base
def create_db_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")