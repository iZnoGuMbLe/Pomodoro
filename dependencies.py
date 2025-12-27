from database import session_db
from sqlalchemy.orm import Session

from exception import TokenExpired, TokenNotCorrect
from repository import TaskRepository, CacheTask, UserRepository
from cache import get_redis_connection
from service.auth import AuthService
from service.task_service import TaskService
from fastapi import Depends, security, Security, HTTPException

from service.user_create import UserService
from settings import Settings


def get_task_repository(db_session: Session = Depends(session_db)) -> TaskRepository:
    return TaskRepository(db_session)

def get_cache_task_repository() -> CacheTask:
    redis_connection = get_redis_connection()
    return CacheTask(redis_connection)

def get_task_serv_dep(
    task_repository: TaskRepository = Depends(get_task_repository),
    task_cache: CacheTask = Depends(get_cache_task_repository)
) -> TaskService:

    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache

    )

def get_user_repository(db_session: Session = Depends(session_db))-> UserRepository:
    return UserRepository(db_session=db_session)



def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository)
) -> AuthService:
    return AuthService(user_repository=user_repository,settings=Settings())


def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        auth_service: AuthService = Depends(get_auth_service)
) -> UserService:
    return UserService(user_repository=user_repository,user_auth_service=auth_service)

reusable_oauth2 = security.HTTPBearer()


def get_request_user_id(
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