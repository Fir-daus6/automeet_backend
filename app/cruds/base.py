from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import update as sql_update
from pydantic import BaseModel
import asyncio

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], soft_delete: bool = False):
        """
        Generic CRUD class for Automeet project.
        - model: SQLAlchemy model class
        - soft_delete: True if this model should be soft-deleted
        """
        self.model = model
        self.soft_delete = soft_delete

    async def get(self, db: AsyncSession, id: Any, with_relationships: bool = True) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id)
        if with_relationships:
            query = query.options(selectinload("*"))  # eager load all relationships
        result = await db.execute(query)
        return result.scalars().first()

    async def get_multi(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        search: Optional[str] = None,
        with_relationships: bool = True
    ) -> List[ModelType]:
        query = select(self.model)
        if filters:
            for attr, value in filters.items():
                query = query.where(getattr(self.model, attr) == value)
        if search:
            # simple search across all string columns
            for column in self.model.__table__.columns:
                if str(column.type) == "VARCHAR":
                    query = query.where(column.ilike(f"%{search}%"))
        if with_relationships:
            query = query.options(selectinload("*"))
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        obj_data = obj_in.dict(exclude_unset=True)
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        obj_data = obj_in.dict(exclude_unset=True) if isinstance(obj_in, BaseModel) else obj_in
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, db_obj: ModelType) -> ModelType:
        if self.soft_delete:
            setattr(db_obj, "is_active", False)
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
        else:
            await db.delete(db_obj)
            await db.commit()
        return db_obj

    # Extra: increment views or attendance
    async def increment_field(self, db: AsyncSession, db_obj: ModelType, field: str, amount: int = 1) -> ModelType:
        current_value = getattr(db_obj, field, 0) or 0
        setattr(db_obj, field, current_value + amount)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
