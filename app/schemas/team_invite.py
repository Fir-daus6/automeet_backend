from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

from app.schemas.team_roles import TeamRoleSchema
from .base_schema import BaseUUIDSchema, BaseResponseSchema, BaseTotalCountResponseSchema
from .base_filters import BaseFilters
from .users import UserSchema 


class TeamInviteBaseSchema(BaseModel):
    email: EmailStr = Field(..., description="Email of the invited user")
    role_id: Optional[str] = Field(None, description="UUID of the role assigned to the invitee")
    invited_by_uuid: Optional[str] = Field(None, description="UUID of the user who sent the invite")
    status: Optional[str] = Field("pending", description="Invitation status (pending, accepted, expired, revoked)")


class TeamInviteCreateSchema(TeamInviteBaseSchema):
    pass


class TeamInviteUpdateSchema(TeamInviteBaseSchema):
    pass


class TeamInviteSchema(TeamInviteBaseSchema, BaseUUIDSchema):
    role: Optional[TeamRoleSchema] = Field(None, description="Role assigned to the invitee")
    invited_by: Optional[UserSchema] = Field(None, description="User who sent the invitation")
    created_at: Optional[datetime] = Field(None, description="Timestamp when the invite was created")


class TeamInviteResponseSchema(BaseResponseSchema):
    data: Optional[TeamInviteSchema] = None


class TeamInviteListResponseSchema(BaseResponseSchema):
    data: Optional[List[TeamInviteSchema]] = None


class TeamInviteTotalCountListResponseSchema(BaseTotalCountResponseSchema):
    data: Optional[List[TeamInviteSchema]] = None


class TeamInviteFilters(BaseFilters):
    email: Optional[str] = Field(None, description="Filter by invited email")
    role_id: Optional[str] = Field(None, description="Filter by role UUID")
    invited_by_uuid: Optional[str] = Field(None, description="Filter by inviter UUID")
    status: Optional[str] = Field(None, description="Filter by invitation status")
    search: Optional[str] = Field(None, description="Search by email or status")