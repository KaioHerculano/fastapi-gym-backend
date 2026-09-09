from typing import Optional
from uuid import UUID

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.accounts import Student, Teacher, User


async def user_email_exists(
    db: AsyncSession, email: str, exclude_user_id: Optional[UUID] = None
) -> bool:

    query = select(exists().where(User.email == email))

    if exclude_user_id:
        query = select(
            exists().where(
                (User.email == email) & (User.id != exclude_user_id)
            )
        )

    return await db.scalar(query)


async def create_user(db: AsyncSession, user: User) -> User:
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


async def updated_user(
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


async def check_user_exists(db: AsyncSession, user_id: UUID) -> bool:

    query = select(exists().where(User.id == user_id))

    return await db.scalar(query)


async def check_student_user_id_exists(
    db: AsyncSession, user_id: UUID
) -> bool:

    query = select(exists().where(Student.user_id == user_id))

    return await db.scalar(query)


async def check_student_cpf_exists(db: AsyncSession, cpf: str) -> bool:

    query = select(exists().where(Student.cpf == cpf))

    return await db.scalar(query)


async def check_student_email_exists(
    db: AsyncSession, email: str, exclude_student_id: Optional[UUID] = None
) -> bool:

    query = select(exists().where(Student.email == email))

    if exclude_student_id:
        query = select(
            exists().where(
                (Student.email == email) & (Student.id != exclude_student_id)
            )
        )

    return await db.scalar(query)


async def create_student(db: AsyncSession, student: Student) -> Student:

    db.add(student)
    await db.commit()
    await db.refresh(student)

    return student


async def list_students(
    db: AsyncSession,
    offset: int,
    limit: int,
    search: Optional[str] = None,
) -> Student:

    query = select(Student).where(Student.is_active)

    if search:
        search_filter = f'%{search}%'
        query = query.where(
            Student.cpf.ilike(search_filter)
            | Student.full_name.ilike(search_filter)
            | Student.email.ilike(search_filter)
            | Student.emergency_contact_name.ilike(search_filter)
        )

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    return list(result.scalars().all())


async def get_student(db: AsyncSession, student_id: UUID) -> Optional[Student]:
    return await db.get(Student, student_id)


async def updated_student(db: AsyncSession, student: Student) -> Student:

    db.add(student)
    await db.commit()
    await db.refresh(student)

    return student


async def delete_student(db: AsyncSession, student: Student):

    db.add(student)
    await db.commit()


async def check_teacher_user_id_exists(
    db: AsyncSession, user_id: UUID
) -> bool:

    query = select(exists().where(Teacher.user_id == user_id))

    return await db.scalar(query)


async def check_teacher_cref_exists(
    db: AsyncSession, cref: str, exclude_teacher_id: Optional[UUID] = None
) -> bool:

    query = select(exists().where(Teacher.cref == cref))

    if exclude_teacher_id:
        query = select(
            exists().where(
                (Teacher.cref == cref) & (Teacher.id != exclude_teacher_id)
            )
        )

    return await db.scalar(query)


async def check_teacher_email_exists(
    db: AsyncSession, email: str, exclude_teacher_id: Optional[UUID] = None
) -> bool:

    query = select(exists().where(Teacher.email == email))

    if exclude_teacher_id:
        query = select(
            exists().where(
                (Teacher.email == email) & (Teacher.id != exclude_teacher_id)
            )
        )

    return await db.scalar(query)


async def create_teacher(db: AsyncSession, teacher: Teacher) -> Teacher:

    db.add(teacher)
    await db.commit()
    await db.refresh(teacher)
    return teacher


async def list_teachers(
    db: AsyncSession, offset: int, limit: int, search: Optional[str] = None
) -> Teacher:

    query = select(Teacher).where(Teacher.is_active)

    if search:
        search_filter = f'%{search}%'
        query = query.where(
            Teacher.cref.ilike(search_filter)
            | Teacher.full_name.ilike(search_filter)
            | Teacher.email.ilike(search_filter)
            | Teacher.phone.ilike(search_filter)
        )

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    return list(result.scalars().all())


async def get_teacher(db: AsyncSession, teacher_id: UUID) -> Optional[Teacher]:
    return await db.get(Teacher, teacher_id)


async def updated_teacher(db: AsyncSession, teacher: Teacher) -> Teacher:

    db.add(teacher)
    await db.commit()
    await db.refresh(teacher)

    return teacher


async def delete_teacher(db: AsyncSession, teacher: Teacher):

    db.add(teacher)
    await db.commit()
