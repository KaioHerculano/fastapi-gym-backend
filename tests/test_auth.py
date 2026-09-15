import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.accounts import RoleEnum, User


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, admin_user: User):
    response = await client.post(
        '/api/v1/login',
        json={'email': admin_user.email, 'password': 'Admin12345'},
    )
    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'


@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient, admin_user: User):
    response = await client.post(
        '/api/v1/login',
        json={'email': admin_user.email, 'password': 'SenhaErrada123'},
    )
    assert response.status_code == 401
    assert response.json()['detail'] == 'Could not validate credentials'


@pytest.mark.asyncio
async def test_login_inactive_user(
    client: AsyncClient, db_session: AsyncSession
):
    inactive_user = User(
        email='inactive@gym.com',
        password=get_password_hash('Password123'),
        role=RoleEnum.STUDENT,
        is_active=False,
    )
    db_session.add(inactive_user)
    await db_session.commit()

    response = await client.post(
        '/api/v1/login',
        json={'email': 'inactive@gym.com', 'password': 'Password123'},
    )
    assert response.status_code == 403
    assert response.json()['detail'] == 'Usuário inativo.'
