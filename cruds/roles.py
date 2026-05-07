from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.roles import Role


class CRUDRole:
    model = Role

    async def get(self, db: AsyncSession, *, uuid: str | None = None, **kwargs: Any) -> Role | None:
        if uuid is None:
            return None
        res = await db.execute(select(Role).where(Role.uuid == uuid))
        return res.scalar_one_or_none()

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        limit: int = 100,
        uuid: list[str] | str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        stmt = select(Role)
        if uuid is not None:
            uuids = [uuid] if isinstance(uuid, str) else [u.strip() for u in uuid if str(u).strip()]
            stmt = stmt.where(Role.uuid.in_(uuids))
        if limit is not None and limit >= 0:
            stmt = stmt.limit(limit)
        res = await db.execute(stmt)
        rows = list(res.scalars().all())
        return {"data": rows, "total_count": len(rows)}


role_crud = CRUDRole()
