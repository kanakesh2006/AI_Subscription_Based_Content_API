from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True, nullable=False)

    password_hash = Column(String, nullable=False)

    role = Column(String, default="free")

    subscription_expiry = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False)

    body = Column(Text, nullable=False)

    is_premium = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)


class AccessLog(Base):
    __tablename__ = "access_logs"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    content_id = Column(Integer, ForeignKey("content.id"))

    ip_address = Column(String)

    access_time = Column(DateTime, default=datetime.utcnow)