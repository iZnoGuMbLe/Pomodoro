from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from typing import Annotated

from starlette.responses import RedirectResponse

from dependencies import get_auth_service
from exception import UserNotFound, UserIncorrectPassword
from schema import UserLoginSchema, UserCreateSchema
from service.auth import AuthService

router = APIRouter(prefix='/auth',tags=['authorization'])

@router.post(
    '/login',
    response_model=UserLoginSchema
)

async def login(
        body: UserCreateSchema,
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:
        return auth_service.login(body.username, body.password)
    except UserNotFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )
    except UserIncorrectPassword as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )


@router.get(
    "/login/google",
    response_class=RedirectResponse
)
async def google_login(
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    redirect_url = auth_service.get_google_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get(
    "/google"
)
async def google_auth(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        code: str
    ):
    return auth_service.google_auth(code=code)


@router.get(
    "/login/yandex",
)

async def yandex_login(
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    redirect_uri = auth_service.get_yandex_redirect_uri()
    print(redirect_uri)
    return RedirectResponse(redirect_uri)

@router.get(
    "/yandex"
)
async def yandex_auth(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        code: str
    ):
    return auth_service.yandex_auth(code=code)


