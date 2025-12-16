from database import session_db
from sqlalchemy.orm import Session
from repository import TaskRepository, CacheTask, UserRepository
from cache import get_redis_connection
from service.auth import AuthService
from service.task_service import TaskService
from fastapi import Depends

from service.user_create import UserService


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
        task_repository=get_task_repository(),
        task_cache=get_cache_task_repository()

    )

def get_user_repository(db_session: Session = Depends(session_db))-> UserRepository:
    return UserRepository(db_session=db_session)


def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(user_repository=user_repository)

def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository)
) -> AuthService:
    return AuthService(user_repository=user_repository)