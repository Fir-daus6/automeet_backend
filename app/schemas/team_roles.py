from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from .base_schema import BaseUUIDSchema, BaseResponseSchema, BaseTotalCountResponseSchema
from .base_filters import BaseFilters
from .users import UserSchema  # Assuming you have this schema


class TeamRoleBaseSchema(BaseModel):
    name: str = Field(..., description="Name of the team role")
    description: Optional[str] = Field(None, description="Description of the team role")


class TeamRoleCreateSchema(TeamRoleBaseSchema):
    pass


class TeamRoleUpdateSchema(TeamRoleBaseSchema):
    pass


class TeamRoleSchema(TeamRoleBaseSchema, BaseUUIDSchema):
    members: Optional[List[UserSchema]] = Field(
        None, description="List of users who have this role"
    )
    created_at: Optional[datetime] = Field(
        None, description="Timestamp when the team role was created"
    )


class TeamRoleResponseSchema(BaseResponseSchema):
    data: Optional[TeamRoleSchema] = None


class TeamRoleListResponseSchema(BaseResponseSchema):
    data: Optional[List[TeamRoleSchema]] = None


class TeamRoleTotalCountListResponseSchema(BaseTotalCountResponseSchema):
    data: Optional[List[TeamRoleSchema]] = None


class TeamRoleFilters(BaseFilters):
    name: Optional[str] = Field(None, description="Filter by role name")
    description: Optional[str] = Field(None, description="Filter by role description")
    search: Optional[str] = Field(
        None, description="Search by role name or description"
    )

