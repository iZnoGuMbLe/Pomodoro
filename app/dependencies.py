import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.client import GoogleClient, YandexClient
from app.infrastructure.database.db_accessor import session_db

from app.exception import TokenExpired, TokenNotCorrect
from app.repository import TaskRepository, CacheTask, UserRepository
from app.infrastructure.cache import get_redis_connection
from app.service.auth import AuthService
from app.service.task_service import TaskService
from fastapi import Depends, security, Security, HTTPException

from app.service.user_create import UserService
from app.settings import Settings


async def get_task_repository(db_session: AsyncSession = Depends(session_db)) -> TaskRepository:
    return TaskRepository(db_session)

async def get_cache_task_repository() -> CacheTask:
    redis_connection = get_redis_connection()
    return CacheTask(redis_connection)

async def get_task_serv_dep(
    task_repository: TaskRepository = Depends(get_task_repository),
    task_cache: CacheTask = Depends(get_cache_task_repository)
) -> TaskService:

    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache

    )

async def get_user_repository(db_session: AsyncSession = Depends(session_db))-> UserRepository:
    return UserRepository(db_session=db_session)

async def get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()

async def get_google_client(async_client:httpx.AsyncClient = Depends(get_async_client) ) -> GoogleClient:
    return GoogleClient(settings=Settings(),async_client=async_client)

async def get_yandex_client(async_client:httpx.AsyncClient = Depends(get_async_client)) -> YandexClient:
    return YandexClient(settings=Settings(),async_client=async_client)


async def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
        google_client: GoogleClient = Depends(get_google_client),
        yandex_client: YandexClient = Depends(get_yandex_client)
) -> AuthService:
    return


async def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        auth_service: AuthService = Depends(get_auth_service)
) -> UserService:
    return UserService(user_repository=user_repository,user_auth_service=auth_service)

reusable_oauth2 = security.HTTPBearer()


async def get_request_user_id(
    auth_service: AuthService = Depends(get_auth_service),
    token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2)
                        ) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)

    except TokenExpired as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )
    except TokenNotCorrect as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )
    return user_id