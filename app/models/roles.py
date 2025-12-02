from typing import TYPE_CHECKING, Optional
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.base_class import Base
from .base_mixins import BaseUUIDModelMixin

if TYPE_CHECKING:
    from .role_permissions import RolePermission
    from .user_roles import UserRole
    from .users import User
    from .permissions import Permission
else:
    RolePermission = "RolePermission"
    UserRole = "UserRole"
    User = "User"
    Permission = "Permission"


class Role(Base, BaseUUIDModelMixin):
    __tablename__ = "roles"

    # Role info
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    has_dashboard_access: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    role_permissions: Mapped[list["RolePermission"]] = relationship(
        "RolePermission", back_populates="role"
    )
    permissions: Mapped[list["Permission"]] = relationship(
        "Permission",
        secondary="role_permissions",
        back_populates="roles",
        overlaps="role_permissions",
    )
    user_roles: Mapped[list["UserRole"]] = relationship(
        "UserRole", back_populates="role", overlaps="users"
    )
    users: Mapped[list["User"]] = relationship(
        "User",
        secondary="user_roles",
        primaryjoin="Role.uuid == UserRole.role_uuid",
        secondaryjoin="UserRole.user_uuid == User.uuid",
        overlaps="user_roles",
        viewonly=True,
    )

    # String representation
    def __str__(self) -> str:
        return f"Role ID: {self.uuid}, Name: {self.name}"
