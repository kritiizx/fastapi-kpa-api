KPA Backend Assignment


This project implements two backend APIs for the KPA assignment using FastAPI and PostgreSQL, demonstrating user authentication and profile retrieval.
Setup InstructionsTo get this project up and running on your local machine, follow these steps:

Clone the repository:git clone https://github.com/kritiizx/fastapi-kpa-api

cd fastapi-kpa-api

Navigate into the project directory:cd kpa_backend

Create and activate a Python virtual environment:python -m venv venv

Install dependencies:pip install -r requirements.txt

(Note: This project was developed with Python 3.12.4. Specific versions of passlib==1.7.4 and bcrypt==3.2.0 were explicitly installed to resolve compatibility issues.)

Install PostgreSQL:Download and install PostgreSQL from https://www.postgresql.org/download/. Remember the postgres superuser password you set during installation.Create a PostgreSQL database:Using pgAdmin (the graphical tool that comes with PostgreSQL) or psql (command-line client), create a new database named kpa_db.Configure Environment Variables (.env file):Create a file named .env in the root directory of your Git repository . 

This file is used to store sensitive configuration.
Add the following variables to your .env file, replacing the bracketed values with your actual credentials and secret key:

DATABASE_URL="postgresql://postgres:password@localhost/kpa_db"
SECRET_KEY="Your_secret_key" 
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30


Run the FastAPI application:Ensure your PowerShell is in the root directory of your Git repository .Ensure your virtual environment is active.

Run the server
:uvicorn kpa_backend.main:app --reload

The API will be available at http://127.0.0.1:8000. You can access the interactive API documentation (Swagger UI) at http://127.0.0.1:8000/docs.Technologies
and Tech Stack UsedBackend Framework: Python FastAPI (Version 0.116.1)Database: PostgreSQLORM (Object Relational Mapper): SQLAlchemy (Version 2.0.41)Password Hashing: Passlib (Version 1.7.4) with bcrypt (Version 3.2.0)Authentication: JWT (JSON Web Tokens) using python-joseEnvironment Variables Management: python-dotenvASGI Server: Uvicorn (Version 0.35.0)Implemented APIsThis project implements two APIs as per the assignment requirements:POST /api/v1/auth/loginDescription: Authenticates a user with a phone number and password. 

Upon successful authentication, it returns a JWT access token and basic user details. 
A dummy user (phone: 7760873976, password: to_share@123) is automatically created in the PostgreSQL database on application startup if it doesn't already exist.

Request Body Example (JSON):
{
  "phone": "7760873976",
  "password": "to_share@123"
}
Successful Response Example (200 OK):{
  "status": "success",
  "message": "Login successful",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "name": "Assignment User",
      "email": "assignment.user@example.com",
      "phone": "7760873976"
    }
  }
}
GET /api/v1/user/profileDescription: Retrieves the profile information of the currently authenticated user. This endpoint is protected and requires a valid JWT access token to be provided in the Authorization header.Headers: Authorization: Bearer <your_jwt_token>Successful Response Example (200 OK):{
  "status": "success",
  "message": "User profile fetched successfully",
  "data": {
    "id": 1,
    "name": "Assignment User",
    "email": "assignment.user@example.com",
    "phone": "7760873976"
  }
}



Limitations or Assumptions MadeDummy User for Testing:
 A single dummy user is created on application startup for ease of testing.
 A real-world application would include a user registration API.Basic JWT Implementation: The JWT handling is foundational for demonstration. Production-grade systems often incorporate refresh tokens, token revocation mechanisms, and more robust error handling for token validation.No Advanced Input Validation: While Pydantic models provide basic type and required field validation, more complex validation (e.g., regex for phone numbers, email format strictness beyond basic checks) is not explicitly implemented but can be easily added.No Centralized Error Logging: Error handling primarily relies on FastAPI's HTTPException. Advanced logging to files or external services is not included.Direct Database Table Creation: Database tables are created directly on application startup using SQLAlchemy's Base.metadata.create_all().
For production environments, a dedicated database migration tool (like Alembic) is recommended to manage schema changes gracefully.Optional (Bonus Points) ConsiderationsDockerization: The backend code could be containerized using Docker for easier deployment and environment consistency.Enhanced Input Validation: Implementing more granular and custom input validation rules.Environment-based Configuration: Already implemented using the .env file.Swagger/OpenAPI Integration: FastAPI automatically provides interactive API documentation at /docs and OpenAPI specification at /openapi.json.
