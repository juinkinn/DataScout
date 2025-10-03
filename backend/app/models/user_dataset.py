from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from app.core.config import Base

class UserDataset(Base):
    __tablename__ = "user_datasets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    dataset_ref = Column(String, nullable=False)
    collection_name = Column(String, nullable=False)
    status = Column(String, default="ready")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
