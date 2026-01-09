from dataclasses import dataclass

import pytest

from app.models import UserProfile
from app.schema import UserCreateSchema
from tests.fixtures.users.user_model import UserProfileFactory


@dataclass
class FakeUserRepository:
    async def get_user_by_email(self,email: str) -> None:
        return None

    async def create_user_repo(self,user:UserCreateSchema):
        return UserProfileFactory()

@pytest.fixture
def user_repository():
    return FakeUserRepository()