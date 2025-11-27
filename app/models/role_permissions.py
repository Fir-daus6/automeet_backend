# models/role_permissions.py
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.base_class import Base
from .base_mixins import BaseUUIDModelMixin

if TYPE_CHECKING:
    from .roles import Role
    from .permissions import Permission
else:
    Role = "Role"
    Permission = "Permission"


class RolePermission(Base, BaseUUIDModelMixin):
    __tablename__ = "role_permissions"

    # Foreign keys
    role_uuid: Mapped[str] = mapped_column(String(36), ForeignKey("roles.uuid"), nullable=False, index=True)
    permission_uuid: Mapped[str] = mapped_column(String(36), ForeignKey("permissions.uuid"), nullable=False, index=True)

    # Relationships
    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="role_permissions",
        overlaps="permissions, roles"
    )
    permission: Mapped["Permission"] = relationship(
        "Permission",
        back_populates="role_permissions",
        overlaps="permissions, roles"
    )

    # String representation
    def __str__(self) -> str:
        return (
            f"RolePermission -> Role ID: {self.role_uuid}, "
            f"Permission ID: {self.permission_uuid}"
        )
