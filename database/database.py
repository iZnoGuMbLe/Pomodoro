from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine('postgresql+psycopg2://postgres:password@0.0.0.0:5432/pomodoro')


# import sqlite3
# from settings import Settings
#
# settings = Settings()

Session = sessionmaker(engine)

def session_db() -> Session:
    return Session