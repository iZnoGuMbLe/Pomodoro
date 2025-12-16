import string
from dataclasses import dataclass
from repository.user_repo import UserRepository
from schema import UserLoginSchema
from random import random, choice


@dataclass
class UserService:
    user_repository:UserRepository

    def create_user(self, username: str, password: str) -> UserLoginSchema:
        access_token = self.generate_access_token()
        user = self.user_repository.create_user_repo(username=username,password=password,access_token=access_token)
        return UserLoginSchema(user_id=user.id, access_token=user.access_token)

    @staticmethod
    def generate_access_token() -> str:
        return ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(10))