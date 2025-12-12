from dataclasses import dataclass

from repository.task_repository import get_task_repository
from repository import TaskRepository, CacheTask
from schema.tasks_validation import TaskSchema

@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache:CacheTask

    def get_tasks_service(self):
        cache_task = self.task_cache.get_tasks_c()
        if cache_task is not None:
            return cache_task

        tasks = self.task_repository.get_tasks()
        tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
        self.task_cache.set_tasks_c(tasks_schema)
        return tasks_schema

