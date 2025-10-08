import pandas as pd
import os
from ..database import datasets_db
from sqlalchemy.orm import Session
from app.models.user_dataset import UserDataset
from app.schemas.user_dataset import UserDatasetCreate
from datetime import datetime

def insert_user_dataset(user_id: str, dataset_ref: str, csv_path: str, source: str = "kaggle"):
    collection_name = f"user_{user_id}_datasets"
    collection = datasets_db[collection_name]

    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    records = df.to_dict(orient="records")

    for record in records:
        record["_source"] = source
        record["_dataset_ref"] = dataset_ref
        record["_user_id"] = user_id
        record["_filename"] = os.path.basename(csv_path)

    if records:
        collection.insert_many(records)
    return len(records)

def create_user_dataset(db: Session, user_id: int, data: UserDatasetCreate):
    db_entry = UserDataset(
        user_id=user_id,
        dataset_ref=data.dataset_ref,
        status="imported",
        created_at=datetime.utcnow(),
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_user_datasets(db: Session, user_id: int):
    return db.query(UserDataset).filter(UserDataset.user_id == user_id).all()