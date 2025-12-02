from typing import Optional, List
from pydantic import BaseModel, Field
from .base_schema import BaseSchema, BaseUUIDSchema, BaseResponseSchema, BaseTotalCountResponseSchema
from .base_filters import BaseFilters
from datetime import datetime


class UserRoleBaseSchema(BaseModel):
    user_uuid: str = Field(..., description="UUID of the user associated with the role")
    role_uuid: str = Field(..., description="UUID of the role assigned to the user")
    delete_protection: Optional[bool] = Field(
        True, description="Indicates whether this user-role assignment is protected from deletion"
    )


class UserRoleCreateSchema(UserRoleBaseSchema):
    pass


class RoleSchema(BaseSchema, BaseUUIDSchema):
    name: Optional[str] = Field(None, description="Name of the role")
    description: Optional[str] = Field(None, description="Description of the role")


class UserSchema(BaseSchema, BaseUUIDSchema):
    email: Optional[str] = Field(None, description="Email address of the user")
    username: Optional[str] = Field(None, description="Username of the user")
    first_name: Optional[str] = Field(None, description="First name of the user")
    last_name: Optional[str] = Field(None, description="Last name of the user")
    is_active: Optional[bool] = Field(None, description="Indicates whether the user account is active")
    avatar: Optional[str] = Field(None, description="URL or path to the user's avatar")


class UserRoleSchema(UserRoleBaseSchema, BaseUUIDSchema):
    user: Optional[UserSchema] = Field(None, description="Details of the user")
    role: Optional[RoleSchema] = Field(None, description="Details of the role")
    created_at: Optional[datetime] = Field(None, description="Timestamp when the assignment was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the assignment was last updated")


class UserRoleResponseSchema(BaseResponseSchema):
    data: Optional[UserRoleSchema] = Field(None, description="User-role assignment data")


class UserRoleListResponseSchema(BaseResponseSchema):
    data: Optional[List[UserRoleSchema]] = Field(None, description="List of user-role assignments")


class UserRoleTotalCountListResponseSchema(BaseTotalCountResponseSchema):
    data: Optional[List[UserRoleSchema]] = Field(None, description="List of user-role assignments with total count")


class UserRoleFilters(BaseFilters):
    user_uuid: Optional[str] = Field(None, description="Filter assignments by user UUID")
    role_uuid: Optional[str] = Field(None, description="Filter assignments by role UUID")
    search: Optional[str] = Field(
        None,
        description="Search assignments by user email, username, or role name"
    )
