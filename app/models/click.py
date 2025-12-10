from __future__ import annotations
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base
from datetime import datetime

class Click(Base):

    __tablename__ = "clicks"

    id:Mapped[int] = mapped_column(primary_key=True)
    url_id: Mapped[int] = mapped_column(ForeignKey("urls.id"), nullable=False, index=True)
    clicked_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    url: Mapped[URL] = relationship("URL", back_populates="clicks")
    
