import pytest
import datetime as dt
from jose import jwt

from app.client import GoogleClient
from app.dependencies import get_auth_service
from app.models import UserProfile
from app.schema import UserLoginSchema
from app.service import AuthService
from app.settings import Settings


pytestmark = pytest.mark.asyncio

async def test_get_google_redirect_url__success(
        auth_service_f:AuthService,
        settings:Settings):
    assert settings.google_redirect_url == auth_service_f.get_google_redirect_url()

def test_get_google_redirect_url__fail():
    pass

async def test_generate_access_token__success(auth_service_f:AuthService, settings:Settings):
    user_id = 1
    access_token = auth_service_f.generate_access_token(user_id=user_id)
    decoded_access_token = jwt.decode(access_token,settings.JWT_SECRET_KEY,algorithms=[settings.JWT_ENCODE_ALGO])
    decoded_user_id = decoded_access_token.get('user_id')
    decoded_token_expire = dt.datetime.fromtimestamp(decoded_access_token.get('expire'),tz=dt.timezone.utc)


    assert (decoded_token_expire - dt.datetime.now(tz=dt.UTC)) > dt.timedelta(days=6)
    assert decoded_user_id == user_id


async def test_get_user_id_from_access_token__success(auth_service_f:AuthService):
    user_id = 1
    access_token = auth_service_f.generate_access_token(user_id=user_id)
    decoded_user_id = auth_service_f.get_user_id_from_access_token(access_token)

    assert user_id == decoded_user_id


async def test_google_auth__success(auth_service_f:AuthService,):
    user = await auth_service_f.google_auth(code='fake_code')
    assert user




