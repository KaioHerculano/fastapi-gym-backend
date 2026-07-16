from typing import Optional

from fastapi import APIRouter, status, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists

from app.core.database import get_session
from app.core.security import get_password_hash
from app.models.accounts import User
from app.schemas.accounts import(
    UserCreateSchema,
    UserPublicSchema,
    UserListPublicSchema,
    UserUpdateSchema,
    StudentCreateSchema,
    StudentPublicSchema,
    StudentListPublicSchema,
    StudentUpdateSchema,
    TeacherCreateSchema,
    TeacherPublicSchema,
    TeacherListPublicSchema,
    TeacherUpdateSchema,
)


users_router = APIRouter(prefix="/users", tags=["Usuários"])
students_router = APIRouter(prefix="/students", tags=["Alunos"])
teachers_router = APIRouter(prefix="/teachers", tags=["Professores"])


@users_router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublicSchema,
    summary='Criar novo usuário'
)
async def create_user(
    user: UserCreateSchema,
    db: AsyncSession = Depends(get_session),
):

    email_exist = await db.scalar(
        select(exists().where(User.email == user.email))
    )

    if email_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='E-mail já cadastrado',
        )

    db_user = User(
        email = user.email,
        password = get_password_hash(user.password),
        role = user.role,
        is_active = user.is_active
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user