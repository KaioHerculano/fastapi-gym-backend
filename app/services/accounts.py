from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.accounts import User
from app.repositories.accounts import user_email_exists
from app.repositories.accounts import create_user as create_user_repository
from app.repositories.accounts import list_users as list_users_repository
from app.schemas.accounts import UserCreateSchema


async def create_user(
    db: AsyncSession,
    user: UserCreateSchema,
):
    email_exists = await user_email_exists(db, user.email)

    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='E-mail já cadastrado',
        )

    db_user = User(
        email=user.email,
        password=get_password_hash(user.password),
        role=user.role,
        is_active=user.is_active,
    )

    return await create_user_repository(db, db_user)


async def list_users(
    db: AsyncSession,
    offset: int,
    limit: int,
    search: Optional[str] = None,
):
    users = await list_users_repository(db, offset, limit, search)

    return {
        'users': users,
        'offset': offset,
        'limit': limit,
    }
