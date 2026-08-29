from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.accounts import Student, User
from app.repositories.accounts import (
    check_student_cpf_exists,
    check_student_email_exists,
    check_student_user_id_exists,
    check_user_exists,
    user_email_exists,
)
from app.repositories.accounts import (
    create_student as create_student_repository,
)
from app.repositories.accounts import create_user as create_user_repository
from app.repositories.accounts import delete_user as delete_user_repository
from app.repositories.accounts import delete_student as delete_student_repository
from app.repositories.accounts import get_student as get_student_repository
from app.repositories.accounts import get_user as get_user_repository
from app.repositories.accounts import (
    list_students as list_students_repository,
)
from app.repositories.accounts import list_users as list_users_repository
from app.repositories.accounts import update_user as update_user_repository
from app.repositories.accounts import (
    updated_student as updated_student_repository,
)
from app.schemas.accounts import (
    StudentCreateSchema,
    StudentUpdateSchema,
    UserCreateSchema,
    UserUpdateSchema,
)


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


async def get_user(
    db: AsyncSession,
    user_id: UUID,
):
    user = await get_user_repository(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Usuário não encontrado',
        )

    return user


async def update_user(
    db: AsyncSession,
    user_update: UserUpdateSchema,
    user_id: UUID,
):

    user = await get_user_repository(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Usuário não encontrado',
        )

    update_data = user_update.model_dump(exclude_unset=True)

    if 'email' in update_data and update_data['email'] != user.email:
        email_exists = await user_email_exists(
            db, update_data['email'], exclude_user_id=user_id
        )

        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='E-mail já cadastrado',
            )

    if 'password' in update_data:
        update_data['password'] = get_password_hash(update_data['password'])

    for field, value in update_data.items():
        setattr(user, field, value)

    return await update_user_repository(db, user)


async def delete_user(
    db: AsyncSession,
    user_id: UUID,
):
    user = await get_user_repository(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Usuário não encontrado',
        )

    user.is_active = False

    return await delete_user_repository(db, user)


async def create_student(db: AsyncSession, student: StudentCreateSchema):
    if student.user_id:
        user_exist = await check_user_exists(db, student.user_id)

        if not user_exist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Usuário não encontrado',
            )

        user_id_exist = await check_student_user_id_exists(db, student.user_id)

        if user_id_exist:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Conta já vinculada a outro estudante',
            )

    cpf_exist = await check_student_cpf_exists(db, student.cpf)

    if cpf_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='CPF já cadastrado',
        )

    email_exist = await check_student_email_exists(db, student.email)

    if email_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='E-mail já cadastrado',
        )

    db_student = Student(
        user_id=student.user_id,
        full_name=student.full_name,
        cpf=student.cpf,
        birth_date=student.birth_date,
        phone=student.phone,
        email=student.email,
        emergency_contact_name=student.emergency_contact_name,
        emergency_contact_phone=student.emergency_contact_phone,
        is_active=student.is_active,
    )

    return await create_student_repository(db, db_student)


async def list_students(
    db: AsyncSession,
    offset: int,
    limit: int,
    search: Optional[str] = None,
):
    students = await list_students_repository(db, offset, limit, search)

    return {
        'students': students,
        'offset': offset,
        'limit': limit,
    }


async def get_student(db: AsyncSession, student_id: UUID):
    student = await get_student_repository(db, student_id)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Estudante não encontrado',
        )

    return student


async def updated_student(
    db: AsyncSession,
    student_update: StudentUpdateSchema,
    student_id: UUID,
):
    student = await get_student(db, student_id)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Estudante não encontrado',
        )

    update_data = student_update.model_dump(exclude_unset=True)

    if 'email' in update_data and update_data['email'] != student.email:
        email_exists = await check_student_email_exists(
            db, update_data['email'], exclude_student_id=student_id
        )

        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='E-mail já cadastrado',
            )

    for field, value in update_data.items():
        setattr(student, field, value)

    return await updated_student_repository(db, student)


async def delete_student(
    db: AsyncSession,
    student_id: UUID
):
    student = await get_student_repository(db, student_id)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Estudante não encontrado',
        )

    if not student.is_active:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Estudante já deletado',
        )

    student.is_active = False

    return await delete_student_repository(db, student)