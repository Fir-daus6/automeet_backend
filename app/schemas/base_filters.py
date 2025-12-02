from typing import Optional
from pydantic import BaseModel, Field

class BaseFilters(BaseModel):
    """
    BaseFilters provides common query parameters for filtering, pagination, 
    sorting, and including related entities in Automeet API endpoints.
    """

    skip: Optional[int] = Field(
        0,
        description="Number of items to skip before returning the result set (pagination offset).",
        example=0,
    )
    limit: Optional[int] = Field(
        10,
        description="Maximum number of items to return in the result set.",
        example=50,
    )
    sort: Optional[str] = Field(
        "created_at:desc",
        description="Sorting criteria in the format 'field:direction' (e.g., 'first_name:asc' or 'created_at:desc').",
        example="first_name:asc",
    )
    include_relations: Optional[str] = Field(
        None,
        description="Comma-separated list of related models to include (e.g., 'roles,profile,teams').",
        example="roles,profile",
    )
    fields: Optional[str] = Field(
        None,
        description="Comma-separated list of specific fields to include in the response (e.g., 'uuid,first_name,email').",
        example="uuid,first_name,email",
    )
    search: Optional[str] = Field(
        None,
        description="Search term to filter results by matching across multiple fields (e.g., 'user name, email, or team').",
        example="john",
        pattern=r"""^(?i)[\p{L}\p{N}\s]+(?:[.,'\-\s][\p{L}\p{N}\s]+)*[.]?$""",
    )
    search_fields: Optional[str] = Field(
        None,
        description=(
            "Comma-separated list of fields to perform search in. Can include direct fields "
            "(e.g., 'first_name,email') and related model fields (e.g., 'profile.bio,roles.name'). "
            "If omitted, all string fields of the model are used by default."
        ),
        example="first_name,last_name,email,profile.bio,roles.name",
    )
