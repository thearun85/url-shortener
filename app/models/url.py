from __future__ import annotations
from sqlalchemy import String, DateTime, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base
from datetime import datetime

class URL(Base):

    __tablename__ = "urls"
    id: Mapped[int] = mapped_column(primary_key=True)
    original_url: Mapped[str] = mapped_column(Text, nullable=False)
    short_code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    clicks: Mapped[list[Click]] = relationship("Click", back_populates="url", cascade="all, delete-orphan")
