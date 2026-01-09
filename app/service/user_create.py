
from dataclasses import dataclass
from app.repository.user_repo_fixt import UserRepository
from app.schema import UserLoginSchema

from app.service.auth import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    user_auth_service: AuthService

    async def create_user(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.create_user_repo(username=username, password=password)
        access_token = self.user_auth_service.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

