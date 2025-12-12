from fastapi import APIRouter,status, Depends
from typing import Annotated

from dependencies import get_task_repository, get_cache_task_repository, get_task_serv_dep
from repository import TaskRepository, CacheTask
from database.database import session_db
from schema.tasks_validation import TaskSchema
from service import TaskService

router = APIRouter(prefix='/task123',tags=['task'])

@router.get('/all', response_model=list[TaskSchema])
async def get_tasks(task_service: Annotated[TaskService,Depends(get_task_serv_dep)]):
    return task_service.get_tasks_service()



@router.post('/task_body', response_model=TaskSchema)
async def create_task(task_body:TaskSchema,
    task_repository: Annotated[TaskRepository,Depends(get_task_repository)]
                      ):
    task_id = task_repository.create_task(task_body)
    task_body.id = task_id
    return task_body


@router.patch('/{task_id}', response_model=TaskSchema)
async def update_task(
        task_id: int,
        name: str,
        pomodoro_count: int,
        task_repository: Annotated[TaskRepository,Depends(get_task_repository)]
        ):
    return task_repository.update_t(task_id,name,pomodoro_count)




@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int,
                      task_repository: Annotated[TaskRepository,Depends(get_task_repository)]
                      ):
    return task_repository.delete_task(task_id)



