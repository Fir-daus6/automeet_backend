from datetime import date, datetime
from typing import List, Optional, Literal, Annotated
import dns.resolver
from pydantic import BaseModel, EmailStr, Field, constr, field_validator
from .base_schema import BaseResponseSchema, BaseUUIDSchema, BaseTotalCountResponseSchema
from .validate_uuid import UUIDStr
from app.utils.responses import bad_request_response

# Field types
PasswordStr = Annotated[str, constr(min_length=8)]
PhoneStr = Annotated[str, constr(min_length=7, max_length=20)]
GenderType = Literal["male", "female", "other"]

# Base filters
class BaseFilters(BaseModel):
    search: Optional[str] = Field(None, description="Search term for filtering results")


# User base schema
class UserBaseSchema(BaseModel):
    first_name: str = Field(..., description="First name of the user")
    last_name: str = Field(..., description="Last name of the user")
    email: EmailStr = Field(..., description="Email of the user")
    phone_number: Optional[PhoneStr] = Field(None, description="Phone number of the user")
    address: Optional[str] = Field(None, description="Address of the user")
    gender: Optional[str] = Field(None, description="Gender of the user")
    date_of_birth: Optional[date] = Field(None, description="Date of birth of the user")
    bio: Optional[str] = Field(None, description="Short biography of the user")
    status: Optional[str] = Field(None, description="Status of the user")


class EmailValidationSchema(BaseModel):
    email: EmailStr = Field(..., description="Email to validate")

    @field_validator("email")
    def validate_email(cls, value):
        domain = value.split("@")[1]
        try:
            answers = dns.resolver.resolve(domain, "MX")
            if not answers:
                return bad_request_response(f"Email domain {domain} has no MX records")
        except Exception:
            return bad_request_response(f"Email domain {domain} has no MX records")
        return value


class SendVerificationEmailSchema(EmailValidationSchema):
    pass


class ResendSendVerificationCodeSchema(SendVerificationEmailSchema):
    type: Literal["confirm_email", "reset_password", "change_password"] = "confirm_email"


class UserConfirmEmailSchema(EmailValidationSchema):
    code: Annotated[str, constr(min_length=1, max_length=8)]


class UserConfirmForgetPasswordSchema(EmailValidationSchema):
    code: Annotated[str, constr(min_length=1, max_length=8)]
    password: PasswordStr

    @field_validator("password")
    def validate_password_complexity(cls, value):
        if not any(char.isupper() for char in value):
            return bad_request_response("Password must contain an uppercase letter")
        if not any(char.isdigit() for char in value):
            return bad_request_response("Password must contain a digit")
        return value


class UserUpdateWithPasswordSchema(UserBaseSchema):
    password: Optional[PasswordStr] = None


# Admin update schemas
class AdminUpdateUserSchema(BaseModel):
    first_name: Optional[str] = Field(None, description="First name of the user")
    last_name: Optional[str] = Field(None, description="Last name of the user")
    phone_number: Optional[PhoneStr] = Field(None, description="Phone number of the user")
    gender: Optional[str] = Field(None, description="Gender of the user")
    address: Optional[str] = Field(None, description="Address of the user")
    date_of_birth: Optional[date] = Field(None, description="Date of birth of the user")
    status: Optional[str] = Field(None, description="Status of the user")
    role_uuid: Optional[UUIDStr] = Field(None, description="Role UUID assigned to the user")


class AdminUpdateFieldOfficerSchema(BaseModel):
    first_name: Optional[str] = Field(None, description="First name of the user")
    last_name: Optional[str] = Field(None, description="Last name of the user")
    phone_number: Optional[PhoneStr] = Field(None, description="Phone number of the user")
    gender: Optional[str] = Field(None, description="Gender of the user")
    address: Optional[str] = Field(None, description="Address of the user")
    date_of_birth: Optional[date] = Field(None, description="Date of birth of the user")
    status: Optional[str] = Field(None, description="Status of the user")
    is_active: Optional[bool] = Field(None, description="Whether the user is active")


# User create / initialize schemas
class UserCreateSchema(UserBaseSchema):
    password: PasswordStr = Field(..., description="Password for the user")
    confirm_password: PasswordStr = Field(..., description="Confirm password")
    user_type: Literal["user", "company"] = Field("user", description="Type of user")

    @field_validator("password", "confirm_password")
    def validate_password_complexity(cls, value):
        if not any(char.isupper() for char in value):
            return bad_request_response("Password must contain an uppercase letter")
        if not any(char.isdigit() for char in value):
            return bad_request_response("Password must contain a digit")
        return value


class UserInitializeSchema(UserBaseSchema):
    password: PasswordStr = Field(..., description="Password for the user")


# User update / profile schemas
class UserUpdateSchema(UserBaseSchema):
    is_verified: Optional[bool] = Field(None, description="Whether user is verified")
    verified_at: Optional[datetime] = Field(None, description="Datetime of verification")
    is_active: Optional[bool] = Field(None, description="Whether user is active")
    last_login: Optional[datetime] = Field(None, description="Last login datetime")


class UserUpdateProfileSchema(BaseModel):
    first_name: Optional[str] = Field(None, description="First name of the user")
    last_name: Optional[str] = Field(None, description="Last name of the user")
    phone_number: Optional[PhoneStr] = Field(None, description="Phone number of the user")
    gender: Optional[str] = Field(None, description="Gender of the user")
    address: Optional[str] = Field(None, description="Address of the user")
    date_of_birth: Optional[date] = Field(None, description="Date of birth of the user")
    bio: Optional[str] = Field(None, description="Biography of the user")


# Roles
class UserRoleSchema(BaseUUIDSchema):
    name: Optional[str] = Field(None, description="Role name")
    label: Optional[str] = Field(None, description="Role label")
    description: Optional[str] = Field(None, description="Role description")


class UserRoleWithoutRoutesSchema(UserRoleSchema):
    pass


# User responses
class UserWithoutRoutesSchema(UserUpdateSchema, BaseUUIDSchema):
    roles: Optional[List[UserRoleWithoutRoutesSchema]] = None


class UserSchema(UserUpdateSchema, BaseUUIDSchema):
    roles: Optional[List[UserRoleSchema]] = None


class GenericUserSchema(UserBaseSchema, BaseUUIDSchema):
    is_verified: bool = False
    is_active: bool = False
    verified_at: Optional[datetime] = None


class UserResponseSchema(BaseResponseSchema):
    data: Optional[UserSchema] = None


class UserResponseWithoutRoutesSchema(BaseResponseSchema):
    data: Optional[UserWithoutRoutesSchema] = None


class UserListResponseSchema(BaseResponseSchema):
    data: Optional[List[UserSchema]] = None


class UserTotalCountListResponseSchema(BaseTotalCountResponseSchema):
    data: Optional[List[UserWithoutRoutesSchema]] = None


class UserLoginResponseSchema(BaseResponseSchema):
    access_token: str
    refresh_token: str
    data: Optional[UserSchema] = None


class UserFilters(BaseFilters):
    email: Optional[EmailStr] = Field(None, description="Email of the user")
    first_name: Optional[str] = Field(None, description="First name of the user")
    last_name: Optional[str] = Field(None, description="Last name of the user")
    is_active: Optional[bool] = Field(None, description="Whether user is active")
    is_verified: Optional[bool] = Field(None, description="Whether user is verified")
    status: Optional[str] = Field(None, description="Status of the user")
