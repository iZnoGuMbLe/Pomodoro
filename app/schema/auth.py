from pydantic import BaseModel, Field


class GoogleUserData(BaseModel):
    sub: str
    email: str
    name: str
    google_access_token: str

class YandexUserData(BaseModel):
    login: str
    id: str
    name: str = Field(alias="real_name")
    default_email: str
    access_token: str
    sex: str