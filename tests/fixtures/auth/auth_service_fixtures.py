import pytest

from app.service import AuthService
from app.settings import Settings



@pytest.fixture
def auth_service_f(yandex_client_f,google_client_f, user_repository):
    return AuthService(user_repository=user_repository,
                       settings=Settings(),
                       google_client=google_client_f,
                       yandex_client=yandex_client_f
                       )