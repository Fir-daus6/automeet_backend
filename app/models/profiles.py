from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING

from ..database.base_class import Base
from .base_mixins import BaseUUIDModelMixin

if TYPE_CHECKING:
    from .users import User
else:
    User = "User"

class Profile(Base, BaseUUIDModelMixin):
    __tablename__ = "profiles"

    name: Mapped[str] = mapped_column(String(100), nullable= False)
    email: Mapped[str] = mapped_column(String(100), nullable= False)
    department: Mapped[str] = mapped_column(String(100), nullable=True)
    bio: Mapped[str] = mapped_column(Text, nullable=True)    
    user_uuid: Mapped[str] = mapped_column(String(36), ForeignKey("users.uuid", ondelete="CASCADE"), unique=True, nullable=False)

    users: Mapped["User"] = relationship("User", back_populates="profile")

def __str__(self):
    return f"Profile(full_name={self.full_name}, email={self.email})"