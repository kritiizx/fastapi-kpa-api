# kpa_backend/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import timedelta

from .database import engine, SessionLocal, Base, get_db, create_db_tables
from .models import User
from .schemas import UserLogin, LoginResponse, APIResponse, ProfileResponse, UserResponseData
from .auth import get_password_hash, verify_password, create_access_token, get_current_user
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create FastAPI app instance
app = FastAPI(
    title="KPA Backend Assignment API",
    description="Backend APIs for KPA assignment using FastAPI and PostgreSQL.",
    version="1.0.0",
)

# Event handler for application startup
@app.on_event("startup")
async def startup_event():
    # Create database tables if they don't exist
    create_db_tables()
    print("Database setup complete.")

    # Add a dummy user for testing if not already present
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.phone == "7760873976").first():
            hashed_password = get_password_hash("to_share@123")
            dummy_user = User(
                phone="7760873976",
                password_hash=hashed_password,
                name="Assignment User",
                email="assignment.user@example.com"
            )
            db.add(dummy_user)
            db.commit()
            db.refresh(dummy_user)
            print(f"Dummy user created: {dummy_user.phone}")
        else:
            print("Dummy user already exists.")
    except Exception as e:
        print(f"Error during dummy user creation: {e}")
        db.rollback()
    finally:
        db.close()

# Dependency for database session
db_dependency = Annotated[Session, Depends(get_db)]

# --- API Endpoints ---

@app.post("/api/v1/auth/login", response_model=LoginResponse, summary="User Login")
async def login_for_access_token(user_credentials: UserLogin, db: db_dependency):
    """
    Authenticates a user with phone number and password.
    Returns an access token and user details upon successful login.
    """
    user = db.query(User).filter(User.phone == user_credentials.phone).first()

    if not user or not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid phone number or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    # Prepare user data for response
    user_data = UserResponseData(
        id=user.id,
        name=user.name,
        email=user.email,
        phone=user.phone
    )

    return LoginResponse(
        status="success",
        message="Login successful",
        data={
            "token": access_token,
            "user": user_data.dict() # Convert Pydantic model to dictionary
        }
    )



# kpa_backend/main.py (continued from login endpoint)

@app.get("/api/v1/user/profile", response_model=ProfileResponse, summary="Get User Profile")
async def get_user_profile(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Retrieves the profile information of the authenticated user.
    Requires a valid JWT token in the Authorization header.
    """
    user_data = UserResponseData(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        phone=current_user.phone
    )
    return ProfileResponse(
        status="success",
        message="User profile fetched successfully",
        data=user_data
    )