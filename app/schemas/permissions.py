from typing import Optional, List
from pydantic import BaseModel, Field
from .base_schema import BaseUUIDSchema, BaseResponseSchema, BaseTotalCountResponseSchema
from .base_filters import BaseFilters


class PermissionBaseSchema(BaseModel):
    name: str = Field(..., description="Unique name of the permission")
    label: Optional[str] = Field(None, description="Short label for the permission")
    description: Optional[str] = Field(None, description="Detailed description of the permission")
    type: str = Field("I", description="Type of the permission, default is 'I'")


class PermissionCreateSchema(PermissionBaseSchema):
    pass


class PermissionUpdateSchema(PermissionBaseSchema):
    pass


class PermissionSchema(PermissionBaseSchema, BaseUUIDSchema):
    pass


class PermissionResponseSchema(BaseResponseSchema):
    data: Optional[PermissionSchema] = None


class PermissionListResponseSchema(BaseResponseSchema):
    data: Optional[List[PermissionSchema]] = None


class PermissionTotalCountListResponseSchema(BaseTotalCountResponseSchema):
    data: Optional[List[PermissionSchema]] = None


class PermissionFilters(BaseFilters):
    name: Optional[str] = Field(None, description="Filter by permission name")
    label: Optional[str] = Field(None, description="Filter by permission label")
    description: Optional[str] = Field(None, description="Filter by permission description")
    type: Optional[str] = Field(None, description="Filter by permission type")
    search: Optional[str] = Field(
        None, description="Search by name, label, or description"
    )
