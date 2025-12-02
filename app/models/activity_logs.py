from typing import Union, Optional
from sqlalchemy import ForeignKey, String, Boolean, JSON, Text, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..database.base_class import Base
from .base_mixins import BaseIDModelMixin
from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .users import User
else:
    User = "User"


class ActivityLog(BaseIDModelMixin, Base):
    """Activity log model for tracking user actions."""

    __tablename__ = "activity_logs"

    # The user who performed the action
    user_uuid: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("users.uuid"), nullable=True
    )

    # The type of entity affected (e.g., "Meeting", "Message", "User")
    entity: Mapped[str] = mapped_column(String(50), nullable=False)

    # Snapshot of data before and after the action
    previous_data: Mapped[Optional[Union[dict, list]]] = mapped_column(
        JSON, nullable=True, default={}
    )
    new_data: Mapped[Optional[Union[dict, list]]] = mapped_column(
        JSON, nullable=True, default={}
    )

    # Action type and description
    action: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., "create", "update"
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Optional extra flags
    delete_protection: Mapped[bool] = mapped_column(Boolean, default=True)

    # Timestamps inherited from BaseIDModelMixin
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationship
    user: Mapped[Optional["User"]] = relationship(
        "User", back_populates="activity_logs"
    )

    def __str__(self) -> str:
        return (
            f"ActivityLog(id={self.id}, entity={self.entity}, "
            f"action={self.action}, user_uuid={self.user_uuid})"
        )
