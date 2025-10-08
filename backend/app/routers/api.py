from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user_dataset import UserDatasetCreate, UserDatasetResponse
from app.schemas.user import UserCreate, UserResponse, Token
from app.crud.user_dataset import create_user_dataset, get_user_datasets
from app.crud.user import authenticate_user, create_user, get_user_by_username
from app.services import add_dataset_to_collection, search_kaggle
from app.core.security import create_access_token
from .dependencies import get_current_user
from app.database.postgresql_database import get_db

router = APIRouter()

@router.get("/search")
def search_datasets(query: str):
    return search_kaggle(query)

@router.post("/datasets/import")
def import_dataset(dataset_ref: str, current_user=Depends(get_current_user)):
    return add_dataset_to_collection(dataset_ref, current_user.id)

@router.post("/datasets", response_model=UserDatasetResponse)
def create_dataset(
    data: UserDatasetCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_user_dataset(db, current_user.id, data)


@router.get("/datasets/me", response_model=list[UserDatasetResponse])
def list_my_datasets(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_user_datasets(db, current_user.id)

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status

@router.post("/auth/register", response_model=UserResponse)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_username(db, user_in.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    user = create_user(db, user_in)
    return user

@router.post("/auth/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/auth/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user
