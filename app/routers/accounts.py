from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import get_current_user
from app.models.accounts import Student, Teacher, User
from app.schemas.accounts import (
    StudentCreateSchema,
    StudentListPublicSchema,
    StudentPublicSchema,
    StudentUpdateSchema,
    TeacherCreateSchema,
    TeacherListPublicSchema,
    TeacherPublicSchema,
    TeacherUpdateSchema,
    UserCreateSchema,
    UserListPublicSchema,
    UserPublicSchema,
    UserUpdateSchema,
)
from app.services.accounts import create_student as create_student_service
from app.services.accounts import create_user as create_user_service
from app.services.accounts import get_student as get_student_service
from app.services.accounts import get_user as get_user_service
from app.services.accounts import list_students as list_students_service
from app.services.accounts import list_users as list_users_service
from app.services.accounts import update_user as update_user_service
from app.services.accounts import updated_student as updated_student_service
from app.services.accounts import delete_user as delete_user_service
from app.services.accounts import delete_student as delete_student_service

users_router = APIRouter(
    prefix='/users',
)
students_router = APIRouter(
    prefix='/students',
)
teachers_router = APIRouter(
    prefix='/teachers',
)


@users_router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublicSchema,
    summary='Criar novo usuário',
)
async def create_user(
    user: UserCreateSchema,
    db: AsyncSession = Depends(get_session),
):
    return await create_user_service(db, user)


@users_router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=UserListPublicSchema,
    summary='Listar todos os usuários',
)
async def list_users(
    offset: int = Query(0, ge=0, description='Número de registros para pular'),
    limit: int = Query(
        100, ge=1, le=100, description='Limite de registros por página'
    ),
    search: Optional[str] = Query(None, description='Buscar por e-mail'),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    return await list_users_service(db, offset, limit, search)


@users_router.get(
    path='/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=UserPublicSchema,
    summary='Buscar usuário pelo ID',
)
async def get_user(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    return await get_user_service(db, user_id)


@users_router.patch(
    path='/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=UserPublicSchema,
    summary='Atualizar usuário',
)
async def update_user(
    user_id: UUID,
    user_update: UserUpdateSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):

    return await update_user_service(db, user_update, user_id)


@users_router.delete(
    path='/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Deletar usuário',
)
async def delete_user(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):

    return await delete_user_service(db, user_id)


@students_router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=StudentPublicSchema,
    summary='Criar novo estudante',
)
async def create_student(
    student: StudentCreateSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    return await create_student_service(db, student)


@students_router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=StudentListPublicSchema,
    summary='Listar todos os estudantes',
)
async def list_students(
    offset: int = Query(0, ge=0, description='Número de registros para pular'),
    limit: int = Query(
        100, ge=1, le=100, description='Limite de registros por página'
    ),
    search: Optional[str] = Query(
        None,
        description='Buscar por CPF, nome, e-mail ou contato de emergência',
    ),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    return await list_students_service(db, offset, limit, search)


@students_router.get(
    path='/{student_id}',
    status_code=status.HTTP_200_OK,
    response_model=StudentPublicSchema,
    summary='Buscar estudante pelo ID',
)
async def get_student(
    student_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    return await get_student_service(db, student_id)


@students_router.patch(
    path='/{student_id}',
    status_code=status.HTTP_200_OK,
    response_model=StudentPublicSchema,
    summary='Atualizar estudante',
)
async def updated_student(
    student_id: UUID,
    student_update: StudentUpdateSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    return await updated_student_service(db, student_update, student_id)


@students_router.delete(
    path='/{student_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Deletar estudante',
)
async def delete_student(
    student_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):

    return await delete_student_service(db, student_id)


@teachers_router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=TeacherPublicSchema,
    summary='Criar novo professor',
)
async def create_teacher(
    teacher: TeacherCreateSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    teacher_user_exist = await db.scalar(
        select(exists().where(User.id == teacher.user_id))
    )

    if not teacher_user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Usuário não encontrado',
        )

    teacher_user_id_exist = await db.scalar(
        select(exists().where(Teacher.user_id == teacher.user_id))
    )

    if teacher_user_id_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Conta já vinculada a outro professor',
        )

    cref_exist = await db.scalar(
        select(exists().where(Teacher.cref == teacher.cref))
    )

    if cref_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='CREF já cadastrado',
        )

    email_exist = await db.scalar(
        select(exists().where(Teacher.email == teacher.email))
    )

    if email_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='E-mail já cadastrado',
        )

    db_techer = Teacher(
        user_id=teacher.user_id,
        full_name=teacher.full_name,
        cref=teacher.cref,
        phone=teacher.phone,
        email=teacher.email,
        specialty=teacher.specialty,
        is_active=teacher.is_active,
    )

    db.add(db_techer)
    await db.commit()
    await db.refresh(db_techer)

    return db_techer


@teachers_router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=TeacherListPublicSchema,
    summary='Listar todos os professores Ativos',
)
async def list_teachers(
    offset: int = Query(0, ge=0, description='Número de registros para pular'),
    limit: int = Query(
        100, ge=1, le=100, description='Limite de registros por página'
    ),
    search: Optional[str] = Query(
        None, description='Buscar por CREF, nome, e-mail ou telefone'
    ),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    query = select(Teacher).where(Teacher.is_active)

    if search:
        search_fielter = f'%{search}%'
        query = query.where(
            Teacher.cref.ilike(search_fielter)
            | Teacher.full_name.ilike(search_fielter)
            | Teacher.email.ilike(search_fielter)
            | Teacher.phone.ilike(search_fielter)
        )

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    teachers = result.scalars().all()

    return {
        'teachers': teachers,
        'offset': offset,
        'limit': limit,
    }


@teachers_router.get(
    path='/{teacher_id}',
    status_code=status.HTTP_200_OK,
    response_model=TeacherPublicSchema,
    summary='Buscar professor pelo ID',
)
async def get_teacher(
    teacher_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    teacher = await db.get(Teacher, teacher_id)

    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Professor não encontrado',
        )

    return teacher


@teachers_router.patch(
    path='/{teacher_id}',
    status_code=status.HTTP_200_OK,
    response_model=TeacherPublicSchema,
    summary='Atualizar professor',
)
async def updated_teacher(
    teacher_id: UUID,
    teacher_update: TeacherUpdateSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    teacher = await db.get(Teacher, teacher_id)

    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Professor não encontrado',
        )

    update_data = teacher_update.model_dump(exclude_unset=True)

    if 'cref' in update_data and update_data['cref'] != teacher.cref:
        cref_exists = await db.scalar(
            select(
                exists().where(
                    (Teacher.cref == update_data['cref'])
                    & (Teacher.id != teacher_id)
                )
            )
        )

        if cref_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='CREF já cadastrado',
            )

    if 'email' in update_data and update_data['email'] != teacher.email:
        email_exists = await db.scalar(
            select(
                exists().where(
                    (Teacher.email == update_data['email'])
                    & (Teacher.id != teacher_id)
                )
            )
        )

        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='E-mail já cadastrado',
            )

    for fild, value in update_data.items():
        setattr(teacher, fild, value)

    await db.commit()
    await db.refresh(teacher)

    return teacher


@teachers_router.delete(
    path='/{teacher_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Deletar professor',
)
async def delete_teacher(
    teacher_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    teacher = await db.get(Teacher, teacher_id)

    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Professor não encontrado',
        )

    if teacher.is_active:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Professor já deletado',
        )

    teacher.is_active = False

    db.add(teacher)
    await db.commit()
