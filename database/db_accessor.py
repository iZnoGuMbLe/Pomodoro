from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from settings import Settings

settings = Settings()

engine = create_engine(settings.db_url)


Session = sessionmaker(engine)

def session_db() -> Session:
    return Session