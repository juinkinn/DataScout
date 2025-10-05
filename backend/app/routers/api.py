from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas.user_dataset import UserDatasetCreate, UserDatasetResponse
from ..crud.user_dataset import create_user_dataset, get_user_datasets
from ..database.postgresql_database import get_db
from ..services import add_dataset_to_collection, search_kaggle

router = APIRouter()

@router.get("/search")
def search_datasets(query: str):
    return search_kaggle(query)

@router.post("/datasets/import")
def import_dataset(dataset_ref: str, user_id: int):
    result = add_dataset_to_collection(dataset_ref, user_id)
    return result

@router.post("/datasets/{user_id}", response_model=UserDatasetResponse)
def create_dataset(user_id: int, data: UserDatasetCreate, db: Session = Depends(get_db)):
    return create_user_dataset(db, user_id, data)

@router.get("/datasets/{user_id}", response_model=list[UserDatasetResponse])
def list_datasets(user_id: int, db: Session = Depends(get_db)):
    return get_user_datasets(db, user_id)
