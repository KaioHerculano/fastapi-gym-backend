from typing import Optional
from enum import Enum
from uuid import uuid4, UUID

from datetime import datetime

from sqlalchemy import DateTime, func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class RoleEnum(str, Enum):
    ADMIN = 'ADMIN'
    TEACHER = 'TEACHER'
    RECEPTIONIST = 'RECEPTIONIST'
    STUDENT = 'STUDENT'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str]
    role: Mapped[RoleEnum] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey('users.id'))
    full_name: Mapped[str] = mapped_column(String(150))
    cpf: Mapped[str] = mapped_column(String(11), unique=True)
    birth_date: Mapped[datetime] = mapped_column(DateTime)
    phone: Mapped[str] = mapped_column(String(15))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    emergency_contact_phone: Mapped[str] = mapped_column(String(15))
    emergency_contact_name: Mapped[str] = mapped_column(String(150))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )


class Teacher(Base):
    __tablename__ = 'teachers'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey('users.id'))
    full_name: Mapped[str] = mapped_column(String(150))
    cref: Mapped[str] = mapped_column(String(20), unique=True)
    phone: Mapped[str] = mapped_column(String(15))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    specialty: Mapped[Optional[str]] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )
    