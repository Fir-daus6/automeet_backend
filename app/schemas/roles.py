from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base_schema import BaseUUIDSchema, BaseResponseSchema, BaseTotalCountResponseSchema
from .base_filters import BaseFilters
from .permissions import PermissionSchema  
from .users import UserSchema  


class RoleBaseSchema(BaseModel):
    name: str = Field(..., description="Name of the role")
    has_dashboard_access: Optional[bool] = Field(
        False, description="Whether users with this role have dashboard access"
    )


class RoleCreateSchema(RoleBaseSchema):
    pass


class RoleUpdateSchema(RoleBaseSchema):
    pass


class RoleSchema(RoleBaseSchema, BaseUUIDSchema):
    permissions: Optional[List[PermissionSchema]] = Field(
        None, description="List of permissions associated with the role"
    )
    users: Optional[List[UserSchema]] = Field(
        None, description="List of users assigned to this role"
    )
    created_at: Optional[datetime] = Field(
        None, description="Timestamp when the role was created"
    )


class RoleResponseSchema(BaseResponseSchema):
    data: Optional[RoleSchema] = None


class RoleListResponseSchema(BaseResponseSchema):
    data: Optional[List[RoleSchema]] = None


class RoleTotalCountListResponseSchema(BaseTotalCountResponseSchema):
    data: Optional[List[RoleSchema]] = None


class RoleFilters(BaseFilters):
    name: Optional[str] = Field(None, description="Filter by role name")
    has_dashboard_access: Optional[bool] = Field(
        None, description="Filter roles by dashboard access permission"
    )
    search: Optional[str] = Field(
        None, description="Search by role name or related attributes"
    )
