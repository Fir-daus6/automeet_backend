from typing import TYPE_CHECKING, Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.base_class import Base
from .base_mixins import BaseUUIDModelMixin

if TYPE_CHECKING:
    from .role_permissions import RolePermission
    from .roles import Role
else:
    RolePermission = "RolePermission"
    Role = "Role"


class Permission(Base, BaseUUIDModelMixin):
    __tablename__ = "permissions"

    # Permission fields
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    label: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    type: Mapped[str] = mapped_column(
        String(2), default="I", nullable=False
    )  

    # Relationships
    role_permissions: Mapped[list["RolePermission"]] = relationship(
        "RolePermission", back_populates="permission"
    )
    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary="role_permissions",
        back_populates="permissions",
        overlaps="role_permissions",
    )

    # String representation
    def __str__(self) -> str:
        return f"Permission -> ID: {self.uuid}, Name: {self.name}"
