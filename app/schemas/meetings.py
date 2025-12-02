from datetime import date, time, datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from .base_schema import BaseUUIDSchema, BaseResponseSchema, BaseTotalCountResponseSchema, BaseSchema
from .base_filters import BaseFilters


class MeetingBaseSchema(BaseModel):
    title: str = Field(..., description="Title of the meeting")
    scheduled_on: date = Field(..., description="Date when the meeting is scheduled")
    scheduled_at: time = Field(..., description="Time when the meeting is scheduled")
    duration: int = Field(..., description="Duration of the meeting in minutes")
    platform: str = Field(..., description="Platform used for the meeting (e.g., Zoom, Teams)")
    participant: str = Field(..., description="Participants of the meeting, usually comma-separated emails or names")
    description: str = Field(..., description="Description or agenda of the meeting")
    user_uuid: str = Field(..., description="UUID of the user who created the meeting")


class MeetingCreateSchema(MeetingBaseSchema):
    pass


class MeetingUpdateSchema(MeetingBaseSchema):
    pass


class MeetingSchema(MeetingBaseSchema, BaseUUIDSchema):
    pass


class MeetingResponseSchema(BaseResponseSchema):
    data: Optional[MeetingSchema] = None


class MeetingListResponseSchema(BaseResponseSchema):
    data: Optional[List[MeetingSchema]] = None


class MeetingTotalCountListResponseSchema(BaseTotalCountResponseSchema):
    data: Optional[List[MeetingSchema]] = None


class MeetingFilters(BaseFilters):
    title: Optional[str] = Field(None, description="Filter by meeting title")
    scheduled_on: Optional[date] = Field(None, description="Filter by scheduled date")
    scheduled_at: Optional[time] = Field(None, description="Filter by scheduled time")
    duration: Optional[int] = Field(None, description="Filter by duration in minutes")
    platform: Optional[str] = Field(None, description="Filter by meeting platform")
    participant: Optional[str] = Field(None, description="Filter by participants")
    user_uuid: Optional[str] = Field(None, description="Filter by UUID of the user who created the meeting")
