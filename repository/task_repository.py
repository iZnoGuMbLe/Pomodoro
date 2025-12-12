from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from database import Tasks, Categories
from database.database import session_db
from schema.tasks_validation import TaskSchema


class TaskRepository:


    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_tasks(self):
        with self.db_session() as session:
            task_ses: list[Tasks] = session.execute(select(Tasks)).scalars().all()
        return task_ses

    def get_one_task(self, task_id: int) -> Tasks | None:
        with self.db_session() as session:
            task: Tasks = session.execute(select(Tasks).where(Tasks.id == task_id)).scalar_one_or_none()
        return task

    def create_task(self, task: TaskSchema) -> int:
        task_model = Tasks(name=task.name, pomodoro_count=task.pomodoro_count,category_id=task.category_id)
        with self.db_session() as session:
            session.add(task_model)
            session.flush()
            new_id = task_model.id
            session.commit()
        return new_id

    def delete_task(self, task_id: int):
        with self.db_session() as session:
            session.execute(delete(Tasks).where (Tasks.id == task_id))
            session.commit()

    def get_task_by_cat_name(self,category_name: str) -> list[Tasks]:
        query = select(Tasks).join(Categories, Tasks.category_id == Categories.id).where(Categories.name == category_name)
        with self.db_session() as session:
            task: list[Tasks] = session.execute(query).scalars()
        return task

    def update_t(self,task_id: int, name: str, pomodoro_count: int) -> Tasks:
        query = update(Tasks).where(Tasks.id == task_id).values(name=name, pomodoro_count=pomodoro_count).returning(Tasks.id)
        with self.db_session() as session:
            task_id_upd: int = session.execute(query).scalar_one_or_none()
            session.commit()
            return self.get_one_task(task_id_upd)



def get_task_repository() -> TaskRepository:
    db_session = session_db()
    return TaskRepository(db_session)