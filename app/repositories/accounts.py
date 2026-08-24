from typing import Optional
from uuid import UUID

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.accounts import User, Student


async def user_email_exists(
    db: AsyncSession,
    email: str,
    exclude_user_id: Optional[UUID] = None
) -> bool:

    query = select(exists().where(User.email == email))

    if exclude_user_id:
        query = select(exists().where(
            (User.email == email) &
            (User.id != exclude_user_id)
        ))

    return await db.scalar(query)


async def create_user(
    db: AsyncSession,
    user: User
) ->  User:
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
    query = select(User).where(User.is_active)

    if search:
        search_filter = f'%{search}%'
        query = query.where(User.email.ilike(search_filter))

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    return list(result.scalars().all())


async def get_user(db: AsyncSession, user_id: UUID) -> Optional[User]:
    return await db.get(User, user_id)


async def update_user(
    db: AsyncSession,
    user: User,
) -> User:

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def delete_user(
    db: AsyncSession,
    user: User,
):

    db.add(user)
    await db.commit()


async def check_user_exists(
    db: AsyncSession,
    user_id: UUID
) -> bool:

    query = select(exists().where(User.id == user_id))

    return await db.scalar(query)


async def check_student_user_id_exists(
    db: AsyncSession,
    user_id: UUID 
) -> bool:

    query = select(exists().where(Student.user_id == user_id))

    return await db.scalar(query)


async def check_student_cpf_exists(
    db: AsyncSession,
    cpf: str
) -> bool:

    query = select(exists().where(Student.cpf == cpf))

    return await db.scalar(query)
