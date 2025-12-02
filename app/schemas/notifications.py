from typing import Optional, List
from pydantic import BaseModel, Field
from .base_schema import BaseUUIDSchema, BaseResponseSchema, BaseTotalCountResponseSchema
from .base_filters import BaseFilters


class NotificationSettingsBaseSchema(BaseModel):
    recording: Optional[bool] = Field(True, description="Whether recording notifications are enabled")
    transcription: Optional[bool] = Field(True, description="Whether transcription notifications are enabled")
    action_items: Optional[bool] = Field(True, description="Whether action items notifications are enabled")
    team_invitations: Optional[bool] = Field(True, description="Whether team invitation notifications are enabled")
    meeting_reminders: Optional[bool] = Field(True, description="Whether meeting reminder notifications are enabled")
    user_uuid: str = Field(..., description="UUID reference to the user these settings belong to")


class NotificationSettingsCreateSchema(NotificationSettingsBaseSchema):
    pass


class NotificationSettingsUpdateSchema(NotificationSettingsBaseSchema):
    pass


class NotificationSettingsSchema(NotificationSettingsBaseSchema, BaseUUIDSchema):
    pass


class NotificationSettingsResponseSchema(BaseResponseSchema):
    data: Optional[NotificationSettingsSchema] = None


class NotificationSettingsListResponseSchema(BaseResponseSchema):
    data: Optional[List[NotificationSettingsSchema]] = None


class NotificationSettingsTotalCountListResponseSchema(BaseTotalCountResponseSchema):
    data: Optional[List[NotificationSettingsSchema]] = None


class NotificationSettingsFilters(BaseFilters):
    user_uuid: Optional[str] = Field(None, description="Filter by the user UUID")
    recording: Optional[bool] = Field(None, description="Filter by recording notification setting")
    transcription: Optional[bool] = Field(None, description="Filter by transcription notification setting")
    action_items: Optional[bool] = Field(None, description="Filter by action items notification setting")
    team_invitations: Optional[bool] = Field(None, description="Filter by team invitations notification setting")
    meeting_reminders: Optional[bool] = Field(None, description="Filter by meeting reminders notification setting")
