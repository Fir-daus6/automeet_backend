from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.users import User


class CRUDUser:
    model = User

    async def get(
        self,
        db: AsyncSession,
        *,
        email: str | None = None,
        uuid: str | None = None,
        soft_deleted: bool | None = None,
        statement=None,
    ) -> User | None:
        if statement is not None:
            res = await db.execute(statement)
            return res.unique().scalar_one_or_none()
        stmt = select(User)
        if email is not None:
            stmt = stmt.where(User.email == email)
        if uuid is not None:
            stmt = stmt.where(User.uuid == uuid)
        if soft_deleted is True:
            stmt = stmt.where(User.soft_deleted.is_(True))
        elif soft_deleted is False:
            stmt = stmt.where(User.soft_deleted.is_(False))
        res = await db.execute(stmt)
        return res.unique().scalar_one_or_none()

    async def create(self, db: AsyncSession, *, obj_in: Any, user_uuid: str) -> User:
        _ = user_uuid
        data = obj_in.model_dump(exclude_unset=True)
        data.pop("role_uuid", None)
        data.setdefault("is_active", True)
        db_obj = User(**data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: User, obj_in: Any, user_uuid: str) -> User:
        _ = user_uuid
        data = obj_in.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def restore(self, db: AsyncSession, *, db_obj: User, fields: dict[str, Any]) -> User:
        for field, value in fields.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def soft_delete(self, db: AsyncSession, *, db_obj: User) -> User:
        db_obj.soft_deleted = True
        db_obj.soft_deleted_at = datetime.now(timezone.utc)  # type: ignore[assignment]
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_with_cache(
        self,
        db: AsyncSession,
        *,
        unique_records: bool = False,
        query_filters: list[Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        _ = unique_records
        skip = kwargs.get("skip", 0) or 0
        limit = kwargs.get("limit", 10)
        search = kwargs.get("search")
        email = kwargs.get("email")
        first_name = kwargs.get("first_name")
        last_name = kwargs.get("last_name")
        is_active = kwargs.get("is_active")
        is_verified = kwargs.get("is_verified")
        status = kwargs.get("status")

        conds: list[Any] = [User.soft_deleted.is_(False)]
        if query_filters:
            conds.extend(query_filters)
        if email:
            conds.append(User.email == email)
        if first_name:
            conds.append(User.first_name.ilike(f"%{first_name}%"))
        if last_name:
            conds.append(User.last_name.ilike(f"%{last_name}%"))
        if is_active is not None:
            conds.append(User.is_active == is_active)
        if is_verified is not None:
            conds.append(User.is_verified == is_verified)
        if status:
            conds.append(User.status == status)
        if search:
            conds.append(
                or_(
                    User.email.ilike(f"%{search}%"),
                    User.first_name.ilike(f"%{search}%"),
                    User.last_name.ilike(f"%{search}%"),
                )
            )

        where_clause = and_(*conds)
        count_stmt = select(func.count()).select_from(User).where(where_clause)
        total = (await db.execute(count_stmt)).scalar() or 0

        stmt = (
            select(User)
            .options(joinedload(User.rbac_roles))
            .where(where_clause)
            .offset(skip)
        )
        if limit is not None and limit > 0:
            stmt = stmt.limit(limit)
        res = await db.execute(stmt)
        data = list(res.unique().scalars().all())
        return {"data": data, "total_count": total}


user_crud = CRUDUser()
