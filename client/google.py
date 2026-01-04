from dataclasses import dataclass
import httpx

from schema import GoogleUserData
from settings import Settings


@dataclass
class GoogleClient:
    settings: Settings
    async_client:httpx.AsyncClient


    async def get_user_info(self,code:str)-> GoogleUserData:
        access_token = await self._get_user_access_token_g(code=code)

        print("ACCESS TOKEN:", access_token)
        async with httpx.AsyncClient() as client:
            user_info = await client.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
        print("STATUS:", user_info.status_code)
        print("TEXT:", user_info.text)

        return GoogleUserData(**user_info.json(), google_access_token=access_token)


    async def _get_user_access_token_g(self, code: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
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