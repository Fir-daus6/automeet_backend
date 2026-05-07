from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_roles import UserRole
from app.schemas.user_roles import UserRoleCreateSchema


class CRUDUserRole:
    model = UserRole

    async def create(
        self,
        db: AsyncSession,
        *,
        obj_in: UserRoleCreateSchema,
        user_uuid: str,
    ) -> UserRole:
        row = UserRole(user_uuid=obj_in.user_uuid, role_uuid=obj_in.role_uuid)
        db.add(row)
        await db.commit()
        await db.refresh(row)
        return row

    async def get(
        self,
        db: AsyncSession,
        *,
        user_uuid: str,
        role_uuid: str,
    ) -> UserRole | None:
        res = await db.execute(
            select(UserRole).where(
                UserRole.user_uuid == user_uuid,
                UserRole.role_uuid == role_uuid,
            )
        )
        return res.scalar_one_or_none()

    async def remove(
        self,
        db: AsyncSession,
        *,
        db_obj: UserRole,
        user_uuid: str,
    ) -> None:
        await db.delete(db_obj)
        await db.commit()

    async def remove_multi(
        self,
        db: AsyncSession,
        *,
        user_uuid: str,
        role_uuid: list[str],
    ) -> None:
        if not role_uuid:
            return
        await db.execute(
            delete(UserRole).where(
                UserRole.user_uuid == user_uuid,
                UserRole.role_uuid.in_(role_uuid),
            )
        )
        await db.commit()


user_roles_crud = CRUDUserRole()
