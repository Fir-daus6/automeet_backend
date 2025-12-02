from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from .base_schema import BaseUUIDSchema, BaseResponseSchema, BaseTotalCountResponseSchema
from .base_filters import BaseFilters


class ProfileBaseSchema(BaseModel):
    name: str = Field(..., description="Full name of the user")
    email: EmailStr = Field(..., description="Email address of the user")
    department: Optional[str] = Field(None, description="Department of the user")
    bio: Optional[str] = Field(None, description="Short biography or description of the user")
    user_uuid: str = Field(..., description="UUID of the associated user")


class ProfileCreateSchema(ProfileBaseSchema):
    pass


class ProfileUpdateSchema(ProfileBaseSchema):
    pass


class ProfileSchema(ProfileBaseSchema, BaseUUIDSchema):
    pass


class ProfileResponseSchema(BaseResponseSchema):
    data: Optional[ProfileSchema] = None


class ProfileListResponseSchema(BaseResponseSchema):
    data: Optional[List[ProfileSchema]] = None


class ProfileTotalCountListResponseSchema(BaseTotalCountResponseSchema):
    data: Optional[List[ProfileSchema]] = None


class ProfileFilters(BaseFilters):
    name: Optional[str] = Field(None, description="Filter by user name")
    email: Optional[str] = Field(None, description="Filter by user email")
    department: Optional[str] = Field(None, description="Filter by user department")
    user_uuid: Optional[str] = Field(None, description="Filter by associated user UUID")
    search: Optional[str] = Field(
        None, description="Search by name, email, or department"
    )
