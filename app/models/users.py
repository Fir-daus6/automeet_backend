# models/user.py
from typing import TYPE_CHECKING, Optional
from datetime import date, datetime
from sqlalchemy import Boolean, DateTime, String, Text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.base_class import Base
from .base_mixins import BaseUUIDModelMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from .codes import VerificationCode
    from .user_roles import UserRole
    from .roles import Role
    from .activity_logs import ActivityLog
else:
    VerificationCode = "VerificationCode"
    UserRole = "UserRole"
    Role = "Role"
    ActivityLog = "ActivityLog"


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
    avatar: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # Verification and activity
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verified_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    verification_codes: Mapped[list["VerificationCode"]] = relationship("VerificationCode", back_populates="user")
    user_roles: Mapped[list["UserRole"]] = relationship("UserRole", back_populates="user", overlaps="roles")
    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary="user_roles",
        primaryjoin="User.uuid == UserRole.user_uuid",
        secondaryjoin="UserRole.role_uuid == Role.uuid",
        overlaps="user_roles",
        viewonly=True,
    )
    activity_logs: Mapped[list["ActivityLog"]] = relationship("ActivityLog", back_populates="user")

    # Helper methods
    def to_schema_dict(self) -> dict:
        base_dict = self.to_dict()
        base_dict["roles"] = [role.to_dict() for role in self.roles]
        return base_dict

    def to_orm_dict(self) -> dict:
        base_dict = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        base_dict["roles"] = [role.to_dict() for role in self.roles]
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
