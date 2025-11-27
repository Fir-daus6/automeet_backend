from sqlalchemy import Boolean, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from ..database.base_class import Base
from .base_mixins import BaseUUIDModelMixin

if TYPE_CHECKING:
    from .users import User
else:
    User = "User"


class NotificationSettings(Base, BaseUUIDModelMixin):
    __tablename__ = "notification_settings"

    recording: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    transcription: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    action_items: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    team_invitations: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    meeting_reminders: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

 
    user_uuid: Mapped[str] = mapped_column(String(36), ForeignKey("users.uuid", ondelete="CASCADE"), unique=True, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="notification_settings")
