from uuid import UUID
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
