from typing import TYPE_CHECKING, Optional
from datetime import date
from sqlalchemy import Boolean, DateTime, String, Text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.notifications import NotificationSettings
from app.models.profiles import Profile
from app.models.team_roles import TeamInvite, TeamRole, team_members_table

from ..database.base_class import Base
from .base_mixins import BaseUUIDModelMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from .codes import VerificationCode
    from .user_roles import UserRole
    from .roles import Role
    from .activity_logs import ActivityLog
    from .meetings import Meeting
else:
    VerificationCode = "VerificationCode"
    UserRole = "UserRole"
    Role = "Role"
    ActivityLog = "ActivityLog"
    Meeting = "Meeting"


class User(Base, BaseUUIDModelMixin, SoftDeleteMixin):
    __tablename__ = "users"

    # Personal info
    first_name: Mapped[str] = mapped_column(String(130), nullable=False)
    last_name: Mapped[str] = mapped_column(String(130), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # Verification and activity
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verified_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # created_at / updated_at from BaseUUIDModelMixin (avoid overriding with incompatible type)

    # Relationships
    verification_codes: Mapped[list["VerificationCode"]] = relationship("VerificationCode", back_populates="user")
    user_roles: Mapped[list["UserRole"]] = relationship("UserRole", back_populates="user", overlaps="rbac_roles")
    rbac_roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary="user_roles",
        primaryjoin="User.uuid == UserRole.user_uuid",
        secondaryjoin="UserRole.role_uuid == Role.uuid",
        overlaps="user_roles",
        viewonly=True,
    )
    activity_logs: Mapped[list["ActivityLog"]] = relationship("ActivityLog", back_populates="user")

    profile: Mapped["Profile"] = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")

    notification_settings: Mapped["NotificationSettings"] = relationship("NotificationSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")

    meetings: Mapped[list["Meeting"]] = relationship("Meeting", back_populates="user")

    team_roles: Mapped[list["TeamRole"]] = relationship(
        "TeamRole",
        secondary=team_members_table,
        back_populates="members",
    )

    team_invites: Mapped[list["TeamInvite"]] = relationship("TeamInvite", back_populates="invited_by")

    @property
    def roles(self) -> list["Role"]:
        """Alias for :attr:`rbac_roles` (API / admin code expects ``user.roles``)."""
        return self.rbac_roles

    # Helper methods
    def to_schema_dict(self) -> dict:
        base_dict = self.to_dict()
        base_dict["roles"] = [role.to_dict() for role in self.rbac_roles]
        base_dict["team_roles"] = [
            {c.name: getattr(tr, c.name) for c in tr.__table__.columns}
            for tr in self.team_roles
        ]
        return base_dict

    def to_orm_dict(self) -> dict:
        base_dict = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        base_dict["roles"] = [role.to_dict() for role in self.rbac_roles]
        base_dict["team_roles"] = [
            {c.name: getattr(tr, c.name) for c in tr.__table__.columns}
            for tr in self.team_roles
        ]
        return base_dict

    # Properties
    @property
    def display_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return self.email

    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email
