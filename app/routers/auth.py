from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import (
    authenticate_user,
    create_access_token,
    get_current_user,
)
from app.models.accounts import User
from app.schemas.auth import LoginRequest, Token

router = APIRouter()


@router.post(
    path='/login',
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary='Gerar token de acesso',
)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_session)
):
    user = await authenticate_user(login_data.email, login_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token = create_access_token(data={'sub': str(user.id)})

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post(
    path='/refresh_token',
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary='Atualizar token de acesso',
)
async def refresh_token(
    current_user: User = Depends(get_current_user)
):
    access_token = create_access_token(data={'sub': str(current_user.id)})

    return {'access_token': access_token, 'token_type': 'bearer'}
