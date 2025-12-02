from typing import Optional, List
from pydantic import BaseModel, Field
from .base_schema import BaseUUIDSchema, BaseResponseSchema, BaseTotalCountResponseSchema
from .base_filters import BaseFilters
from .roles import RoleSchema
from .permissions import PermissionSchema


class RolePermissionBaseSchema(BaseModel):
    role_uuid: str = Field(..., description="UUID of the role")
    permission_uuid: str = Field(..., description="UUID of the permission")


class RolePermissionCreateSchema(RolePermissionBaseSchema):
    pass


class RolePermissionUpdateSchema(RolePermissionBaseSchema):
    pass


class RolePermissionSchema(RolePermissionBaseSchema, BaseUUIDSchema):
    role: Optional[RoleSchema] = Field(
        None, description="The role associated with this permission"
    )
    permission: Optional[PermissionSchema] = Field(
        None, description="The permission associated with this role"
    )


class RolePermissionResponseSchema(BaseResponseSchema):
    data: Optional[RolePermissionSchema] = None


class RolePermissionListResponseSchema(BaseResponseSchema):
    data: Optional[List[RolePermissionSchema]] = None


class RolePermissionTotalCountListResponseSchema(BaseTotalCountResponseSchema):
    data: Optional[List[RolePermissionSchema]] = None


class RolePermissionFilters(BaseFilters):
    role_uuid: Optional[str] = Field(None, description="Filter by role UUID")
    permission_uuid: Optional[str] = Field(None, description="Filter by permission UUID")
    search: Optional[str] = Field(
        None, description="Search by role or permission details"
    )
