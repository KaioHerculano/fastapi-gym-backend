import re
from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from app.models.accounts import RoleEnum


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum
    is_active: bool = True

    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError('Password deve ter no minimo 8 caracteres')
        if not re.search('[a-z]', value):
            raise ValueError(
                'Password deve conter pelo menos uma letra minuscula'
            )
        return value


class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        if value is None:
            return value
        if len(value) < 8:
            raise ValueError('Password deve ter no minimo 8 caracteres')
        if not re.search("[a-z]", value):
            raise ValueError(
                'Password deve conter pelo menos uma letra minuscula'
            )
        return value


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

    @field_validator('full_name')
    def validate_full_name(cls, value: str) -> str:
        if len(value) < 3:
            raise ValueError('Nome deve ter no minimo 3 caracteres')
        return value

    @field_validator("cpf")
    def validate_cpf(cls, value: str) -> str:
        if len(value) != 11:
            raise ValueError('CPF deve ter 11 digitos')
        if not value.isdigit():
            raise ValueError('CPF deve conter apenas digitos')
        return value

    @field_validator('birth_date')
    def validate_birth_date(cls, value: date) -> date:

        if value > date.today():
            raise ValueError('Data de nascimento não pode ser no futuro')
        if value.year < 1900:
            raise ValueError('Data de nascimento invalida')

        today = date.today()

        age = today.year - value.year - (
            (today.month, today.day) < (value.month, value.day)
        )

        if age < 14:
            raise ValueError('O aluno deve ter no minimo 14 anos de idade')

        return value

    @field_validator('phone')
    def validate_phone(cls, value: str) -> str:
        if len(value) not in {10, 11}:
            raise ValueError('Telefone deve ter 10 ou 11 digitos')
        if not value.isdigit():
            raise ValueError('Telefone deve conter apenas digitos')
        return value


class StudentUpdateSchema(BaseModel):
    full_name: Optional[str] = None
    birth_date: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator('full_name')
    def validate_full_name(cls, value: str) -> str:
        if value is None:
            return value
        if len(value) < 3:
            raise ValueError('Nome deve ter no minimo 3 caracteres')
        return value

    @field_validator('birth_date')
    def validate_birth_date(cls, value: date) -> date:
        if value is None:
            return value

        if value > date.today():
            raise ValueError('Data de nascimento não pode ser no futuro')
        if value.year < 1900:
            raise ValueError('Data de nascimento invalida')

        today = date.today()

        age = today.year - value.year - (
            (today.month, today.day) < (value.month, value.day)
        )

        if age < 14:
            raise ValueError('O aluno deve ter no minimo 14 anos de idade')

        return value

    @field_validator('phone')
    def validate_phone(cls, value: str) -> str:
        if value is None:
            return value
        if len(value) not in {10, 11}:
            raise ValueError('Telefone deve ter 10 ou 11 digitos')
        if not value.isdigit():
            raise ValueError('Telefone deve conter apenas digitos')
        return value


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

    @field_validator('full_name')
    def validate_full_name(cls, value: str) -> str:
        if len(value) < 3:
            raise ValueError('Nome deve ter no minimo 3 caracteres')
        return value

    @field_validator('cref')
    def validate_cref(cls, value: str) -> str:
        if len(value) != 11:
            raise ValueError('CREF deve ter 11 caracteres')
        return value

    @field_validator('phone')
    def validate_phone(cls, value: str) -> str:
        if len(value) not in {10, 11}:
            raise ValueError('Telefone deve ter 10 ou 11 digitos')
        if not value.isdigit():
            raise ValueError('Telefone deve conter apenas digitos')
        return value


class TeacherUpdateSchema(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    specialty: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator('full_name')
    def validate_full_name(cls, value: str) -> str:
        if value is None:
            return value
        if len(value) < 3:
            raise ValueError('Nome deve ter no minimo 3 caracteres')
        return value

    @field_validator('phone')
    def validate_phone(cls, value: str) -> str:
        if value is None:
            return value
        if len(value) not in {10, 11}:
            raise ValueError('Telefone deve ter 10 ou 11 digitos')
        if not value.isdigit():
            raise ValueError('Telefone deve conter apenas digitos')
        return value


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
