
from dataclasses import dataclass
from repository.user_repo import UserRepository
from schema import UserLoginSchema

from service.auth import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    user_auth_service: AuthService

    def create_user(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.create_user_repo(username=username, password=password)
        access_token = self.user_auth_service.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

