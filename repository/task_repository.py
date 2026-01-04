from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from models import Tasks, Categories
from database.db_accessor import session_db
from schema import TaskCreateSchema, TaskSchema


class TaskRepository:


    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_tasks(self):
        async with self.db_session as session:
            task_ses: list[Tasks] = (await session.execute(select(Tasks))).scalars().all()
        return task_ses

    async def get_one_task(self, task_id: int) -> Tasks | None:
        async with self.db_session as session:
            task: Tasks = (await session.execute(select(Tasks).where(Tasks.id == task_id))).scalar_one_or_none()
        return task

    async def get_user_task(self, task_id:int,user_id:int,) -> Tasks | None:
        query = select(Tasks).where(Tasks.id==task_id, Tasks.user_id==user_id)
        async with self.db_session as session:
            task: Tasks = (await session.execute(query)).scalar_one_or_none()
        return task



    async def create_task(self, task: TaskCreateSchema, user_id: int) -> int:
        task_model = Tasks(name=task.name,
            pomodoro_count=task.pomodoro_count,
            category_id=task.category_id,
            user_id=user_id)
        async with self.db_session as session:
            session.add(task_model)
            await session.flush()
            new_id = task_model.id
            await session.commit()
        return new_id

    async def delete_task(self, task_id: int, user_id: int):
        async with self.db_session as session:
            await session.execute(delete(Tasks).where (Tasks.id == task_id, Tasks.user_id==user_id))
            await session.commit()

    async def get_task_by_cat_name(self,category_name: str) -> list[Tasks]:
        query = select(Tasks).join(Categories, Tasks.category_id == Categories.id).where(Categories.name == category_name)
        async with self.db_session as session:
            task: list[Tasks] = (await session.execute(query)).scalars()
        return task

    async def update_t(self,task_id: int, name: str, pomodoro_count: int) -> Tasks:
        query = update(Tasks).where(Tasks.id == task_id).values(name=name, pomodoro_count=pomodoro_count).returning(Tasks.id)
        async with self.db_session as session:
            task_id_upd: int = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
            return await self.get_one_task(task_id_upd)



# def get_task_repository() -> TaskRepository:
#     db_session = session_db()
#     return TaskRepository(db_session)