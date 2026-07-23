from uuid import UUID
from typing import Optional

from fastapi import APIRouter, status, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists

from app.core.database import get_session
from app.core.security import get_password_hash
from app.models.accounts import User, Student, Teacher
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


users_router = APIRouter(prefix="/users",)
students_router = APIRouter(prefix="/students",)
teachers_router = APIRouter(prefix="/teachers",)


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


@users_router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=UserListPublicSchema,
    summary='Listar todos os usuários',
)
async def list_users(
    offset: int = Query(0, ge=0, description='Número de registros para pular'),
    limit: int = Query(100, ge=1, le=100, description='Limite de registros por página'),
    search: Optional[str] = Query(None, description='Buscar por e-mail'),
    db: AsyncSession = Depends(get_session)
):
    query = select(User)

    if search:
        search_filter = f'%{search}%'
        query = query.where(User.email.ilike(search_filter))

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    users = result.scalars().all()

    return {
        'users': users,
        'offset': offset,
        'limit': limit,
    }


@users_router.get(
    path='/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=UserPublicSchema,
    summary='Buscar usuário pelo ID',
)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_session),
):
    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Usuário não encontrado',
        )

    return user


@users_router.patch(
    path='/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=UserPublicSchema,
    summary='Atualizar usuário',
)
async def update_user(
    user_id: UUID,
    user_update: UserUpdateSchema,
    db: AsyncSession = Depends(get_session),
):
    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Usuário não encontrado',
        )

    update_data = user_update.model_dump(exclude_unset=True)

    if 'email' in update_data and update_data['email'] != user.email:
        email_exists = await db.scalar(
            select(
                exists().where(
                    (User.email == update_data['email']) &
                    (User.id != user_id)
                )
            )
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

    await db.commit()
    await db.refresh(user)

    return user


@users_router.delete(
    path='/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Deletar usuário',
)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_session),
):
    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Usuário não encontrado',
        )
    
    user.is_active = False

    db.add(user)
    await db.commit()

    return 


@students_router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=StudentPublicSchema,
    summary='Criar novo estudante',
)
async def create_student(
    student: StudentCreateSchema,
    db: AsyncSession = Depends(get_session),
):
    if student.user_id:
        user_exist = await db.scalar(
            select(exists().where(User.id == student.user_id))
        )

        if not user_exist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Usuário não encontrado',
            )

    if student.user_id is not None:
        user_id_exist = await db.scalar(
            select(exists().where(Student.user_id == student.user_id))
        )

        if user_id_exist:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Conta já vinculada a outro estudante',
            )

    cpf_exist = await db.scalar(
        select(exists().where(Student.cpf == student.cpf))
    )

    if cpf_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='CPF já cadastrado',
        )

    email_exist = await db.scalar(
        select(exists().where(Student.email == student.email))
    )

    if email_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='E-mail já cadastrado',
        )

    db_student = Student(
        user_id = student.user_id,
        full_name = student.full_name,
        cpf = student.cpf,
        birth_date = student.birth_date,
        phone = student.phone,
        email = student.email,
        emergency_contact_name = student.emergency_contact_name,
        emergency_contact_phone = student.emergency_contact_phone,
        is_active = student.is_active,
    )

    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)

    return db_student


@students_router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=StudentListPublicSchema,
    summary='Listar todos os estudantes',
)
async def list_students(
    offset: int = Query(0, ge=0, description='Número de registros para pular'),
    limit: int = Query(100, ge=1, le=100, description='Limite de registros por página'),
    search: Optional[str] = Query(None, description='Buscar por CPF, nome, e-mail ou contato de emergência'),
    db: AsyncSession = Depends(get_session)
):
    query = select(Student).where(Student.is_active == True)

    if search:
        search_filter = f'%{search}%'
        query = query.where(Student.cpf.ilike(search_filter) |
                Student.full_name.ilike(search_filter) |
                Student.email.ilike(search_filter) |
                Student.emergency_contact_name.ilike(search_filter)
            )

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    students = result.scalars().all()

    return {
        'students': students,
        'offset': offset,
        'limit': limit,
    }


@students_router.get(
    path='/{student_id}',
    status_code=status.HTTP_200_OK,
    response_model=StudentPublicSchema,
    summary='Buscar estudante pelo ID',
)
async def get_student(
    student_id: UUID,
    db: AsyncSession = Depends(get_session),
):
    student = await db.get(Student, student_id)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Estudante não encontrado',
        )

    return student


@students_router.patch(
    path='/{student_id}',
    status_code=status.HTTP_200_OK,
    response_model=StudentPublicSchema,
    summary='Atualizar estudante',
)
async def updated_student(
    student_id: UUID,
    student_update: StudentUpdateSchema,
    db: AsyncSession = Depends(get_session),
):
    student = await db.get(Student, student_id)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Estudante não encontrado',
        )

    update_data = student_update.model_dump(exclude_unset=True)

    if 'email' in update_data and update_data['email'] != student.email:
        email_exists = await db.scalar(
            select(
                exists().where(
                    (Student.email == update_data['email']) &
                    (Student.id != student_id)
                )
            )
        )

        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='E-mail já cadastrado',
            )

    for field, value in update_data.items():
        setattr(student, field, value)

    await db.commit()
    await db.refresh(student)

    return student


@students_router.delete(
    path='/{student_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Deletar estudante',
)
async def delete_student(
    student_id: UUID,
    db: AsyncSession = Depends(get_session),
):
    student = await db.get(Student, student_id)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Estudante não encontrado',
        )

    if student.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Estudante já deletado',
        )
    
    student.is_active = False

    db.add(student)
    await db.commit()

    return