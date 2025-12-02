from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession
from app.cruds.base import CRUDBase


async def generate_unique_slug(
    db: AsyncSession, 
    crud: CRUDBase, 
    value: str, 
    max_length: int = 255
) -> str:
    base_slug = slugify(value)[:max_length]
    slug = base_slug
    counter = 1

    # Keep incrementing counter until slug is unique
    while await crud.get(db=db, slug=slug) is not None:
        suffix = f"-{counter}"
        # Ensure the slug does not exceed max_length
        slug = f"{base_slug[:max_length - len(suffix)]}{suffix}"
        counter += 1

    return slug


"""
Usage example in Automeet:

from app.cruds.meetings import crud_meeting

slug = await generate_unique_slug(db, crud_meeting, "Team Sync Meeting")
"""
