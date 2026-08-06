from typing import Optional
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.accounts import User


async def user_email_exists(
    db: AsyncSession,
    email: str
) -> bool:
    return await db.scalar(
        select(exists().where(User.email == email))
    )


async def create_user(db: AsyncSession, user: User) ->  User:
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def list_users(
    db: AsyncSession,
    offset: int,
    limit: int,
    search: Optional[str] = None,
):
    query = select(User).where(User.is_active == True)

    if search:
        search_filter = f'%{search}%'
        query = query.where(User.email.ilike(search_filter))

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    return list(result.scalars().all())