from dataclasses import dataclass

from exception import TaskNotFound
from repository import TaskRepository, CacheTask
from schema import TaskCreateSchema
from schema.tasks_validation import TaskSchema

@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache:CacheTask

    def get_tasks_service(self) -> list[TaskSchema]:
        cache_task = self.task_cache.get_tasks_c()
        if cache_task is not None:
            return cache_task

        tasks = self.task_repository.get_tasks()
        tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
        self.task_cache.set_tasks_c(tasks_schema)
        return tasks_schema

    def create_task_service(self, body: TaskCreateSchema, user_id: int) -> TaskSchema:
        task_id = self.task_repository.create_task(body,user_id)
        task = self.task_repository.get_one_task(task_id)
        return TaskSchema.model_validate(task)


    def update_task_name(self,task_id: int, name: str, user_id: int, pomodoro_count: int) -> TaskSchema:
        task = self.task_repository.get_user_task(user_id=user_id,task_id=task_id)
        if not task:
            raise TaskNotFound
        task = self.task_repository.update_t(task_id=task_id,name=name, pomodoro_count=pomodoro_count)
        return TaskSchema.model_validate(task)

    def delete_task(self, task_id:int, user_id:int) -> None:
        task = self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound
        self.task_repository.delete_task(task_id=task_id, user_id=user_id)


