# app/database/base_class.py
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import DeclarativeMeta


class CustomBase:
    # Generate __tablename__ automatically
    @declared_attr  # pyright: ignore[reportArgumentType]
    def __tablename__(cls) -> str:
        return getattr(cls, "__name__", "table").lower()


Base: DeclarativeMeta = declarative_base(cls=CustomBase)
