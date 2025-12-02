from datetime import datetime, timedelta, timezone
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..database.base_class import Base
from app.utils.codes import generate_verification_code
from .base_mixins import BaseIDModelMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
else:
    User = "User"


class VerificationCode(BaseIDModelMixin, Base):
    """Stores OTP / Verification codes for users."""

    __tablename__ = "verification_codes"

    # 6–8 digit generated code (email verification, password reset, etc.)
    code: Mapped[str] = mapped_column(
        String(8),
        nullable=False,
        default=generate_verification_code,
    )

    # Expiration timestamp (12 hours default)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(tz=timezone.utc) + timedelta(hours=12),
        nullable=False,
    )

    # Type of verification (email, password_reset, phone, etc.)
    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="confirm_email",
    )

    # Link to User
    user_uuid: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.uuid"),
        nullable=False,
        index=True,
    )

    user: Mapped["User"] = relationship("User", back_populates="verification_codes")

    def __str__(self) -> str:
        return (
            f"VerificationCode(id={self.id}, code={self.code}, "
            f"type={self.type}, expires_at={self.expires_at}, user_uuid={self.user_uuid})"
        )

    def is_expired(self) -> bool:
        return datetime.now(tz=timezone.utc) >= self.expires_at
