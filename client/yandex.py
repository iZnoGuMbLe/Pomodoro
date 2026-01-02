from dataclasses import dataclass

import requests

from schema import YandexUserData
from settings import Settings

@dataclass
class YandexClient:
    settings: Settings


    def get_user_info_y(self,code:str)-> YandexUserData:
        access_token = self._get_user_access_token_y(code=code)

        print("ACCESS TOKEN:", access_token)

        user_info = requests.get(
            "https://login.yandex.ru/info?format=json",
            headers={"Authorization": f"OAuth {access_token}"}
        )

        print("STATUS:", user_info.status_code)
        print("TEXT:", user_info.text)

        return YandexUserData(**user_info.json(), access_token=access_token)


    def _get_user_access_token_y(self, code: str) -> str:
        response = requests.post(
            "https://oauth.yandex.ru/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": self.settings.YANDEX_CLIENT_ID,
                "client_secret": self.settings.YANDEX_SECRET_KEY,
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )

        print("STATUS:", response.status_code)
        print("TEXT:", response.text)

        response.raise_for_status()
        return response.json()["access_token"]