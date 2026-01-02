from dataclasses import dataclass

import requests

from schema import GoogleUserData
from settings import Settings


@dataclass
class GoogleClient:
    settings: Settings


    def get_user_info(self,code:str)-> GoogleUserData:
        access_token = self._get_user_access_token_g(code=code)

        print("ACCESS TOKEN:", access_token)

        user_info = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        print("STATUS:", user_info.status_code)
        print("TEXT:", user_info.text)

        return GoogleUserData(**user_info.json(), google_access_token=access_token)



    # def _get_user_access_token_g(self,code:str)-> str:
    #     data = {
    #         "code": code,
    #         "client_id": self.settings.GOOGLE_CLIENT_ID,
    #         "client_secret": self.settings.GOOGLE_SECRET_KEY,
    #         "redirect_uri": self.settings.GOOGLE_REDIRECT_URI,
    #         "grant_type": "authorization_code"
    #     }
    #     response = requests.post(self.settings.GOOGLE_TOKEN_URL, data=data)
    #     print(response.status_code)
    #     print(response.text)
    #     return response.json()

    def _get_user_access_token_g(self, code: str) -> str:
        response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": self.settings.GOOGLE_CLIENT_ID,
                "client_secret": self.settings.GOOGLE_SECRET_KEY,
                "redirect_uri": self.settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )

        print("STATUS:", response.status_code)
        print("TEXT:", response.text)

        response.raise_for_status()

        return response.json()["access_token"]