from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserDatasetBase(BaseModel):
    dataset_ref: str

class UserDatasetCreate(UserDatasetBase):
    source: Optional[str] = "kaggle"

class UserDatasetResponse(UserDatasetBase):
    id: int
    user_id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
