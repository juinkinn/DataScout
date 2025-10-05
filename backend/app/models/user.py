from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    conversations = relationship("Conversation", back_populates="user")
