# kpa_backend/schemas.py
from pydantic import BaseModel, Field
from typing import Optional

# Pydantic model for user creation (if we had a registration API)
class UserCreate(BaseModel):
    phone: str = Field(..., example="7760873976")
    password: str = Field(..., example="to_share@123")
    name: Optional[str] = Field(None, example="Rohan Sharma")
    email: Optional[str] = Field(None, example="rohan.sharma@example.com")

# Pydantic model for user login request
class UserLogin(BaseModel):
    phone: str = Field(..., example="7760873976")
    password: str = Field(..., example="to_share@123")

# Pydantic model for user data in responses
class UserResponseData(BaseModel):
    id: int
    name: Optional[str]
    email: Optional[str]
    phone: str

    class Config:
        orm_mode = True # This tells Pydantic to read data from ORM models

# Pydantic model for login response
class LoginResponse(BaseModel):
    status: str = "success"
    message: str = "Login successful"
    data: dict = Field(..., example={"token": "some_jwt_token", "user": {"id": 1, "name": "Rohan Sharma", "email": "rohan.sharma@example.com", "phone": "7760873976"}})

# Pydantic model for general API responses (success/error)
class APIResponse(BaseModel):
    status: str
    message: str

# Pydantic model for profile response
class ProfileResponse(BaseModel):
    status: str = "success"
    message: str = "User profile fetched successfully"
    data: UserResponseData
