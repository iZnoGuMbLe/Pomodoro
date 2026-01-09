from dataclasses import dataclass
import pytest
import httpx

import factory
from factory import fuzzy
from pytest_factoryboy import register
from faker import Factory as FakerFactory

from app.schema import GoogleUserData
from app.settings import Settings

faker = FakerFactory.create()

@dataclass
class FakeGoogleClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> GoogleUserData:
        access_token = await self._get_user_access_token_g(code=code)
        return GoogleUserData(sub = "123456",
            email="test@gmail.com",
            name="Test User",
            google_access_token=access_token)



    async def _get_user_access_token_g(self, code: str) -> str:
        return f'fake_access_token {code}'

@dataclass

class FakeYandexClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info_y(self, code: str) -> dict:
            access_token = await self._get_user_access_token_y(code=code)
            return {'fake_access_token': access_token}


    async def _get_user_access_token_y(self, code: str) -> str:
        return f'fake_access_token {code}'



@pytest.fixture
def google_client_f():
    return FakeGoogleClient(settings=Settings(),async_client=httpx.AsyncClient())

@pytest.fixture
def yandex_client_f():
    return FakeYandexClient(settings=Settings(), async_client=httpx.AsyncClient())


@pytest.fixture
def google_user_info_data() -> GoogleUserData:    # response from google in this test
    return GoogleUserData(
        sub= factory.fuzzy.FuzzyText(length=15),
        email=faker.email(),
        name= faker.name(),
        google_access_token= faker.sha256()
    )