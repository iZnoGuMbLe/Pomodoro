import json

from redis import asyncio as Redis


from schema.tasks_validation import TaskSchema


class CacheTask:
    def __init__(self, redis:Redis):
        self.redis = redis

    async def get_tasks_c(self) -> list[TaskSchema] | None:
        get_task_json = await self.redis.lrange('tasks_c',0,-1)
        if not get_task_json:
            return None

        return [TaskSchema.model_validate(json.loads(task)) for task in get_task_json]


    async def set_tasks_c(self, tasks: list[TaskSchema]):
        if not tasks:
            return

        tasks_json = [task.model_dump_json() for task in tasks]
        async with self.redis as redis:
            await redis.lpush('tasks_c', *tasks_json)
