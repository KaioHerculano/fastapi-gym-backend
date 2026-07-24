from typing import Optional, List
from uuid import UUID

from datetime import datetime, date
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from app.models.accounts import RoleEnum


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum
    is_active: bool = True


class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None


class UserPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserListPublicSchema(BaseModel):
    users: List[UserPublicSchema]
    offset: int
    limit: int


class StudentCreateSchema(BaseModel):
    user_id: Optional[UUID] = None
    full_name: str
    cpf: str
    birth_date: date
    phone: str
    email: EmailStr
    emergency_contact_name: str
    emergency_contact_phone: str
    is_active: bool = True


class StudentUpdateSchema(BaseModel):
    full_name: Optional[str] = None
    birth_date: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    is_active: Optional[bool] = None


class StudentPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: Optional[UUID] = None
    full_name: str
    cpf: str
    birth_date: date
    phone: str
    email: EmailStr
    emergency_contact_name: str
    emergency_contact_phone: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class StudentListPublicSchema(BaseModel):
    students: List[StudentPublicSchema]
    offset: int
    limit: int


class TeacherCreateSchema(BaseModel):
    user_id: UUID
    full_name: str
    cref: str
    phone: str
    email: EmailStr
    specialty: Optional[str] = None
    is_active: bool = True


class TeacherUpdateSchema(BaseModel):
    full_name: Optional[str] = None
    cref: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    specialty: Optional[str] = None
    is_active: Optional[bool] = None


class TeacherPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    full_name: str
    cref: str
    phone: str
    email: EmailStr
    specialty: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class TeacherListPublicSchema(BaseModel):
    teachers: List[TeacherPublicSchema]
    offset: int
    limit: int
