# **py-api-boilerplate** 🚀

A lightweight and scalable FastAPI boilerplate for building high-performance APIs with MySQL using the repository pattern.

## **Features**

✅ FastAPI for modern API development  
✅ SQLModel + SQLAlchemy for database interaction  
✅ Async MySQL support with `aiomysql`  
✅ Pydantic for data validation and settings management  
✅ `.env` support via `python-dotenv`  
✅ Repository pattern for clean architecture  
✅ Scalar for API documentation  
✅ Uvicorn for ASGI server

## **Requirements**

- Python `>=3.10`
- MySQL Server

## **Installation**

1. **Clone the repository**

   ```sh
   git clone https://github.com/your-username/py-api-boilerplate.git
   cd py-api-boilerplate
   ```

2. **Install dependencies using Poetry**

   ```sh
   poetry install
   ```

3. **Set up environment variables**  
   Create a `.env` file:

   ```sh
   cp .env.example .env
   ```

4. **Run the API server**
   ```sh
   poetry run uvicorn app.main:app --reload
   ```

## **Project Structure**

```
py-api-boilerplate/
│── app/
│   ├── api/             # API routes
│   ├── common/
│   │   ├── utilities/   # Utility functions
│   ├── core/
│   │   ├── db/         # Database configuration and connections
│   ├── internal/        # Internal utilities
│   ├── middlewares/     # Custom middlewares
│   ├── models/          # SQLModel database models
│   ├── repositories/    # Data access layer (Repository pattern)
│   ├── services/        # Business logic layer
```

## **Repository Pattern in This Project**

This project follows the **repository pattern** to separate the data access logic from the business logic, ensuring better maintainability and testability.

- **`models/`**: Defines SQLModel database models.
- **`repositories/`**: Handles database operations (CRUD) and abstracts direct queries.
- **`services/`**: Implements business logic by interacting with repositories.

### **Example Usage**

#### **User Model (`models/user.py`)**

```python
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False)
    email: str = Field(unique=True, nullable=False)
```

#### **User Repository (`repositories/user_repository.py`)**

```python
from sqlmodel import Session, select
from app.models.user import User

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int):
        return self.session.exec(select(User).where(User.id == user_id)).first()

    def create(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
```

#### **User Service (`services/user_service.py`)**

```python
from app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_user(self, user_id: int):
        return self.user_repo.get_by_id(user_id)

    def create_user(self, user_data):
        user = User(**user_data)
        return self.user_repo.create(user)
```

#### **API Route (`api/routes/user.py`)**

```python
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.db import get_session
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

router = APIRouter()

@router.get("/users/{user_id}")
def get_user(user_id: int, session: Session = Depends(get_session)):
    user_service = UserService(UserRepository(session))
    return user_service.get_user(user_id)
```

## **Usage**

### **API Documentation**

Once running, visit **Scalar API Docs**:  
📌 `http://127.0.0.1:8000/docs`

### **Example Request (cURL)**

```sh
curl -X 'GET' 'http://127.0.0.1:8000/users/1' -H 'accept: application/json'
```

## **License**

MIT License

---

This boilerplate is designed for scalable and maintainable FastAPI projects using the repository pattern. 🚀
