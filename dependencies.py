from database import session_db
from repository import TaskRepository, CacheTask
from cache import get_redis_connection
from service.task_service import TaskService
from fastapi import Depends



def get_task_repository() -> TaskRepository:
    db_session = session_db()
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