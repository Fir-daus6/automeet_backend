import uuid
from datetime import datetime

from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.base_class import Base
from .base_mixins import BaseUUIDModelMixin



# Many to many
team_members_table = Table(
    "team_members",
    Base.metadata,
    Column("user_uuid", String(36), ForeignKey("users.uuid", ondelete="CASCADE")),
    Column("role_id", String(36), ForeignKey("teamroles.id", ondelete="CASCADE")),
)


class TeamRole(Base):
    __tablename__ = "teamroles"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Users with this role
    members = relationship("User",
        secondary=team_members_table,
        back_populates="roles",
    )

    def __repr__(self):
        return f"<TeamRole {self.name}>"


class TeamInvite(Base, BaseUUIDModelMixin):
    __tablename__ = "teaminvites"

    email: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    role_id: Mapped[str] = mapped_column(String(36), ForeignKey("teamroles.id", ondelete="SET NULL"))
    role = relationship("TeamRole")

    # The user who sent the invitation
    invited_by_uuid: Mapped[str] = mapped_column(String(36), ForeignKey("users.uuid", ondelete="SET NULL"))
    invited_by = relationship("User", foreign_keys=[invited_by_uuid])

    # Invitation status
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)

    # Other options: accepted, expired, revoked
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<TeamInvite email={self.email} status={self.status}>"





