from fastapi import APIRouter, Query
from pydantic import BaseModel
import pandas as pd
from ..services.kaggle_service import search_kaggle, download_kaggle

router = APIRouter()


# --- GET endpoint ---
@router.get("/search")
def search_get(query: str = Query(..., description="Search query")):
    return search_kaggle(query)

@router.post("/datasets/download")
def download_dataset(dataset_ref: str, collection_name: str, user_id: str):
    result = download_kaggle(dataset_ref, collection_name, user_id)
    return result