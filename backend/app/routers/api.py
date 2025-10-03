from fastapi import APIRouter, Query
from pydantic import BaseModel
import pandas as pd
from ..services.kaggle_service import search_kaggle

router = APIRouter()


# --- GET endpoint ---
@router.get("/search")
def search_get(query: str = Query(..., description="Search query")):
    return search_kaggle(query)
