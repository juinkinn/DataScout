from pydantic import BaseModel
from datetime import datetime

class UserDatasetBase(BaseModel):
    dataset_ref: str
    collection_name: str

class UserDatasetCreate(UserDatasetBase):
    pass

class UserDataset(UserDatasetBase):
    id: int
    user_id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
