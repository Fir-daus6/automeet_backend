from datetime import datetime
from typing import Literal, Optional, Annotated
from pydantic import BaseModel, constr
from .base_schema import BaseUUIDSchema, BaseResponseSchema
from .validate_uuid import UUIDStr

# Custom annotated types
TypeStr = Annotated[str, constr(min_length=1, max_length=50)]
CodeStr = Annotated[str, constr(min_length=1, max_length=8)]


# Base schema for verification codes
class VerificationCodeBaseSchema(BaseModel):
    type: TypeStr = "confirm_email"
    user_uuid: UUIDStr
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Schema for creating a verification code
class VerificationCodeCreateSchema(VerificationCodeBaseSchema):
    pass


# Schema for updating a verification code
class VerificationCodeUpdateSchema(VerificationCodeBaseSchema):
    code: CodeStr


# Full schema including UUID and other metadata
class VerificationCodeSchema(VerificationCodeBaseSchema, BaseUUIDSchema):
    code: CodeStr


# Schema for confirming a verification code
class ConfirmVerificationCodeSchema(BaseModel):
    type: Literal["confirm_email", "reset_password", "change_password"] = (
        "confirm_email"
    )
    code: CodeStr


# Response schema for single verification code
class VerificationCodeResponseSchema(BaseResponseSchema):
    data: Optional[VerificationCodeSchema] = None
