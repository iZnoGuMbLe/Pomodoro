from fastapi import APIRouter, status, Depends, HTTPException
from typing import Annotated

from app.dependencies import get_task_repository, get_task_serv_dep, get_request_user_id
from app.exception import TaskNotFound
from app.schema import TaskSchema, TaskCreateSchema
from app.service import TaskService

router = APIRouter(prefix='/task123',tags=['task'])

@router.get('/all', response_model=list[TaskSchema])
async def get_tasks(task_service: Annotated[TaskService,Depends(get_task_serv_dep)]):
    return await task_service.get_tasks_service()



@router.post('/task_body', response_model=TaskSchema)
async def create_task(task_body:TaskCreateSchema,
                      task_service: Annotated[TaskService, Depends(get_task_serv_dep)],
                      user_id:int = Depends(get_request_user_id)):
    task = await task_service.create_task_service(task_body, user_id)
    return TaskSchema.model_validate(task)


@router.patch('/{task_id}', response_model=TaskSchema)
async def update_task(
        task_id: int,
        name: str,
        pomodoro_count: int,
        task_service: Annotated[TaskService, Depends(get_task_serv_dep)],
        user_id: int = Depends(get_request_user_id)
        ):
    try:
        return await task_service.update_task_name(task_id=task_id,name=name,pomodoro_count=pomodoro_count, user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )




@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int,
                      task_service: Annotated[TaskService, Depends(get_task_serv_dep)],
                      user_id:  int = Depends(get_request_user_id)
                      ):
    try:
        await task_service.delete_task(task_id=task_id,user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail)




