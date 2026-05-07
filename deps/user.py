"""Auth dependencies (dev: ``X-Admin-User-UUID`` header). Replace with JWT + permission checks for production."""

from collections.abc import Callable
from typing import Any

from fastapi import Depends, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database.get_session import get_async_session
from app.models.users import User


def get_user_with_permission(_permission: str) -> Callable[..., Any]:
    """
    Return a FastAPI dependency that loads the acting admin user.

    ``_permission`` is reserved for future RBAC checks (e.g. ``can_write_users``).
    """

    async def _dep(
        db: AsyncSession = Depends(get_async_session),
        x_admin_user_uuid: str | None = Header(None, alias="X-Admin-User-UUID"),
    ) -> User:
        if not x_admin_user_uuid:
            from fastapi import HTTPException, status

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing X-Admin-User-UUID header (dev auth).",
            )
        stmt = (
            select(User)
            .options(joinedload(User.rbac_roles))
            .where(User.uuid == x_admin_user_uuid, User.soft_deleted.is_(False))
        )
        res = await db.execute(stmt)
        user = res.unique().scalar_one_or_none()
        if not user:
            from fastapi import HTTPException, status

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid X-Admin-User-UUID.",
            )
        return user

    return _dep
