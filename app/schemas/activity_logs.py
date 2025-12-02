from datetime import datetime, date
from typing import Literal, Optional, List, Union, Dict, Any
from pydantic import BaseModel, Field, model_validator, field_validator, ConfigDict, EmailStr
from .base_schema import BaseSchema, BaseResponseSchema, BaseTotalCountResponseSchema
from .base_filters import BaseFilters
from ..utils.responses import bad_request_response

# Define allowed action types for Automeet
ActionType = Literal[
    "create",
    "update",
    "delete",
    "login",
    "logout",
    "create_password",
    "reset_password",
    "change_password",
    "confirm_email",
    "verify_email",
]

action_choices = [
    "create",
    "update",
    "delete",
    "login",
    "logout",
    "create_password",
    "reset_password",
    "change_password",
    "confirm_email",
    "verify_email",
]


class ActivityLogBaseSchema(BaseModel):
    user_uuid: Optional[str] = Field(
        None, description="UUID of the user who performed the action"
    )
    entity: str = Field(
        ...,
        description="The type of entity affected by the action, e.g., 'Meeting', 'User', 'Message'"
    )
    previous_data: Optional[Union[Dict[str, Any], List[Any]]] = Field(
        None, description="Snapshot of the data before the action was performed"
    )
    new_data: Optional[Union[Dict[str, Any], List[Any]]] = Field(
        None, description="Snapshot of the data after the action was performed"
    )
    action: ActionType = Field(
        ..., description="Type of action performed by the user, e.g., create, update, delete"
    )
    description: Optional[str] = Field(
        None, description="Optional textual description of the action performed"
    )
    delete_protection: Optional[bool] = Field(
        True, description="Indicates whether this log entry is protected from deletion"
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the activity was logged"
    )

    @model_validator(mode="before")
    def convert_datetime_to_isoformat(cls, values):
        if isinstance(values, dict):
            for key, value in values.items():
                if isinstance(value, (datetime, date)):
                    values[key] = value.isoformat()
                elif isinstance(value, dict):
                    values[key] = cls.convert_datetime_to_isoformat(value)
                elif isinstance(value, list):
                    values[key] = [
                        cls.convert_datetime_to_isoformat(item)
                        if isinstance(item, (dict, datetime)) else item
                        for item in value
                    ]
        return values


class ActivityLogCreateSchema(ActivityLogBaseSchema):
    pass


class UserSchema(BaseSchema):
    email: Optional[EmailStr] = Field(None, description="User's email address")
    username: Optional[str] = Field(None, description="User's username")
    first_name: Optional[str] = Field(None, description="User's first name")
    last_name: Optional[str] = Field(None, description="User's last name")
    is_verified: Optional[bool] = Field(None, description="Indicates if the user is verified")
    verified_at: Optional[datetime] = Field(None, description="Timestamp when the user was verified")
    is_active: Optional[bool] = Field(None, description="Indicates if the user account is active")
    avatar: Optional[str] = Field(None, description="URL or path to user's avatar")
    status: Optional[str] = Field(None, description="Custom user status or role description")


class ActivityLogSchema(ActivityLogBaseSchema, BaseSchema):
    user: Optional[UserSchema] = Field(None, description="User details associated with this log")


class ActivityLogResponseSchema(BaseResponseSchema):
    data: Optional[ActivityLogSchema] = Field(None, description="Activity log data")


class ActivityLogListResponseSchema(BaseResponseSchema):
    data: Optional[List[ActivityLogSchema]] = Field(None, description="List of activity logs")


class ActivityLogTotalCountListResponseSchema(BaseTotalCountResponseSchema):
    data: Optional[List[ActivityLogSchema]] = Field(None, description="List of activity logs with total count")


class ActivityLogFilters(BaseFilters):
    model_config = ConfigDict(extra="forbid")
    user_uuid: Optional[str] = Field(
        None, description="Filter logs by the UUID of the user who performed the action"
    )
    entity: Optional[str] = Field(None, description="Filter logs by the affected entity type")
    action: Optional[ActionType] = Field(None, description="Filter logs by the type of action performed")
    exclude_actions: Optional[str] = Field(
        None, description="Comma-separated actions to exclude from the results"
    )
    include_actions: Optional[str] = Field(
        None, description="Comma-separated actions to include in the results"
    )
    start_date: Optional[datetime] = Field(
        None, description="Filter logs starting from this date"
    )
    end_date: Optional[datetime] = Field(
        None, description="Filter logs up to this date"
    )
    search: Optional[str] = Field(
        None, description="Search logs by entity, action, description, or user details"
    )

    @model_validator(mode="after")
    def validate_action_filters(cls, values):
        if values.exclude_actions and values.include_actions:
            return bad_request_response(
                "Cannot use exclude_actions and include_actions together"
            )
        return values

    @field_validator("exclude_actions", "include_actions")
    def validate_actions(cls, value):
        if not value:
            return None
        check_values = [v.strip() for v in value.split(",")]
        for v in check_values:
            if v not in action_choices:
                return bad_request_response(
                    f"Invalid action: {v}. Allowed actions are: {action_choices}"
                )
        return value
