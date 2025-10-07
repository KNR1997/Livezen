from datetime import datetime
from typing import Any, Optional
from uuid import UUID
import bcrypt

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, EmailStr, field_validator
from tortoise import fields, models

from livezen.enums import UserRole
from livezen.models import Pagination, TimestampMixin


class LivezenUser(models.Model):
    id = fields.UUIDField(pk=True, index=True)
    name = fields.TextField(null=True)
    full_name = fields.TextField(null=True)
    first_name = fields.TextField(null=True)
    last_name = fields.TextField(null=True)
    name_with_initials = fields.TextField(null=True)
    username = fields.CharField(max_length=30, null=True)
    email = fields.CharField(max_length=191, unique=True, index=True)
    phone = fields.CharField(max_length=20, null=True)
    nic = fields.TextField(max_length=30, null=True)
    password = fields.TextField()
    is_active = fields.BooleanField(default=True)
    last_login = fields.DatetimeField(null=True)
    role = fields.CharEnumField(UserRole)

    # One-to-one relation (reverse relation)
    profile: fields.OneToOneRelation["Profile"]

    class Meta:
        table = "user"


class Profile(models.Model, TimestampMixin):
    id = fields.BigIntField(pk=True, index=True)
    avatar = fields.JSONField(null=True)
    bio = fields.TextField(null=True)
    socials = fields.TextField(null=True)
    contact = fields.CharField(max_length=20, null=True)
    notifications = fields.JSONField(null=True)

    # One-to-one field to enforce unique link between user and profile
    user: fields.OneToOneRelation[LivezenUser] = fields.OneToOneField(
        "models.LivezenUser",
        related_name="profile",
        on_delete=fields.CASCADE,  # optional: cascade delete profile when user is deleted
    )

    class Meta:
        table = "profile"


def hash_password(password: str) -> str:
    """Hash a password using bcrypt and return as string."""
    pw = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pw, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the hashed one."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


class UserLogin(BaseModel):
    email: str
    password: str


class JWTPayload(BaseModel):
    user_id: str
    email: str
    # is_superuser: bool
    exp: datetime


class JWTOut(BaseModel):
    token: str
    email: str
    username: Optional[str]
    role: str
    permissions: list[str]


class UserRegister(UserLogin):
    full_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    name_with_initials: Optional[str] = None
    username: Optional[str] = None
    email: EmailStr
    password: str
    role: UserRole = UserRole.customer


class UserPasswordUpdate(BaseModel):
    """Pydantic model for password updates only."""

    current_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v):
        """Validate the new password for length and complexity."""
        if not v or len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        if not (any(c.isupper() for c in v) and any(c.islower() for c in v)):
            raise ValueError(
                "Password must contain both uppercase and lowercase characters")
        return v

    @field_validator("current_password")
    @classmethod
    def password_required(cls, v):
        """Ensure the current password is provided."""
        if not v:
            raise ValueError("Current password is required")
        return v


class AdminPasswordReset(BaseModel):
    """Pydantic model for admin password resets."""

    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v):
        """Validate the new password for length and complexity."""
        if not v or len(v) < 8:
            print('less than 8 characters')
            raise RequestValidationError(
                "Password must be at least 8 characters long")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        if not (any(c.isupper() for c in v) and any(c.islower() for c in v)):
            raise ValueError(
                "Password must contain both uppercase and lowercase characters")
        return v


class UserCreate(BaseModel):
    """Pydantic model for creating a new user."""
    name: str | None = None
    full_name: str
    first_name: str
    last_name: str
    name_with_initials: str
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = None

    @field_validator("password", mode="before")
    @classmethod
    def hash(cls, v):
        """Hash the password before storing."""
        return hash_password(str(v))


class ProfileCreate(BaseModel):
    """Pydantic model for creating a new user profile."""
    # avatar: str | None = None
    bio: str | None = None
    # socials: str | None = None
    contact: str | None = None
    notifications: Any | None = None


class UserUpdate(BaseModel):
    """Pydantic model for updating user data."""
    name: str | None = None
    full_name:  str | None = None
    first_name:  str | None = None
    last_name:  str | None = None
    name_with_initials:  str | None = None
    nic: str | None = None
    username:  str | None = None
    email: Optional[EmailStr] = None
    role: str | None = None
    profile: ProfileCreate | None = None


class ProfileRead(BaseModel):
    bio: str | None
    contact: str | None
    notifications: Any | None

    model_config = {
        "from_attributes": True
    }


class UserRead(BaseModel):
    id: UUID
    name: str | None
    full_name: str | None
    first_name: str | None
    last_name: str | None
    name_with_initials: str | None
    nic: str | None
    username: str | None
    email: EmailStr
    role: UserRole
    is_active: bool
    profile: Optional[ProfileRead] = None

    model_config = {
        "from_attributes": True
    }


class UserReadSimple(BaseModel):
    id: UUID
    name: str | None
    full_name: str | None
    first_name: str | None
    last_name: str | None
    name_with_initials: str | None
    nic: str | None
    username: str | None
    email: EmailStr

    model_config = {
        "from_attributes": True
    }


class UserLoginResponse(BaseModel):
    token: str
    role: str
    email: EmailStr
    full_name: str
    permissions: list[str]


class UserPagination(Pagination):
    data: list[UserRead]


class UpdateEmailUserInput(BaseModel):
    email: EmailStr


class ChangePasswordUserInput(BaseModel):
    oldPassword: str
    newPassword: str


class ChangePasswordResponse(BaseModel):
    success: bool
    message: str
