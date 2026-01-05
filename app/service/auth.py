from dataclasses import dataclass

from app.client import GoogleClient
from app.client.yandex import YandexClient
from app.exception import UserNotFound, UserIncorrectPassword, TokenExpired, TokenNotCorrect
from app.models import UserProfile
from app.repository import UserRepository
from app.schema import UserLoginSchema, UserCreateSchema
from jose import jwt, JWTError
import datetime as dt
from datetime import timedelta

from app.settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient
    yandex_client: YandexClient

    async def login(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_name(username)
        self._validate_auth_user(user,password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    @staticmethod
    def _validate_auth_user(user:UserProfile, password:str):
        if not user:
            raise UserNotFound
        if user.password != password:
            raise UserIncorrectPassword


    def generate_access_token(self,user_id:int) -> str:
        expire_date_unix = (dt.datetime.utcnow() + timedelta(days=7)).timestamp()
        token = jwt.encode(
            {'user_id': user_id, 'expire': expire_date_unix},
            self.settings.JWT_SECRET_KEY,
            self.settings.JWT_ENCODE_ALGO )
        return token

    def get_user_id_from_access_token(self,access_token:str) -> int:
        try:
            payload = jwt.decode(access_token,self.settings.JWT_SECRET_KEY,algorithms=[self.settings.JWT_ENCODE_ALGO])
        except JWTError:
            raise TokenNotCorrect
        if payload['expire'] < dt.datetime.utcnow().timestamp():
            raise TokenExpired
        return payload['user_id']

    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url



    async def google_auth(self, code:str):
        user_data = await self.google_client.get_user_info(code=code)
        if user:= await self.user_repository.get_user_by_email(email=user_data.email):
            access_token = self.generate_access_token(user_id=user.id)
            print('user logged in')
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(google_access_token=user_data.google_access_token,
                                            email=user_data.email,
                                             name=user_data.name)
        created_user = await self.user_repository.create_user_repo(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        print('user created')
        return UserLoginSchema(user_id=created_user.id,access_token=access_token)


    def get_yandex_redirect_uri(self) -> str:
        return self.settings.yandex_redirect_uri


    async def yandex_auth(self, code: str):
        user_data = await self.yandex_client.get_user_info_y(code=code)
        if user:= await self.user_repository.get_user_by_email(email=user_data.default_email):
            access_token = self.generate_access_token(user_id=user.id)
            print('user logged in')
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(yandex_access_token=user_data.access_token,
                                            email=user_data.default_email,
                                             name=user_data.name)
        created_user = await self.user_repository.create_user_repo(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        print('user created')
        return UserLoginSchema(user_id=created_user.id,access_token=access_token)




