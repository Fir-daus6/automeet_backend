# models/user_roles.py
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.base_class import Base
from .base_mixins import BaseUUIDModelMixin

if TYPE_CHECKING:
    from .users import User
    from .roles import Role
else:
    Role = "Role"
    User = "User"


class UserRole(Base, BaseUUIDModelMixin):
    __tablename__ = "user_roles"

    # Foreign keys
    role_uuid: Mapped[str] = mapped_column(String(36), ForeignKey("roles.uuid"), index=True, nullable=False)
    user_uuid: Mapped[str] = mapped_column(String(36), ForeignKey("users.uuid"), index=True, nullable=False)

    # Relationships
    role: Mapped["Role"] = relationship(
        "Role", back_populates="user_roles", overlaps="users"
    )
    user: Mapped["User"] = relationship(
        "User", back_populates="user_roles", overlaps="roles"
    )

    # String representation
    def __str__(self) -> str:
        return f"UserRole -> User ID: {self.user_uuid}, Role ID: {self.role_uuid}"
