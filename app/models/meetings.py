from datetime import date, datetime, time
from sqlalchemy import String, ForeignKey, Date, Text, Boolean, Integer, DateTime, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..database.base_class import Base
from .base_mixins import BaseUUIDModelMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
else:
    User = "User"



class Meeting(Base, BaseUUIDModelMixin):
    __tablename__ = "meetings"

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    scheduled_on: Mapped[date] = mapped_column(Date, nullable=False)
    scheduled_at: Mapped[time] = mapped_column(Time, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    platform: Mapped[str] = mapped_column(String(50), nullable=False)
    participant: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    user_uuid: Mapped[str] = mapped_column(String(36), ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="meetings")

def __str__(self) -> str:
    return f"Meeting(title={self.title}, date={self.scheduled_on}, time={self.scheduled_at})"






