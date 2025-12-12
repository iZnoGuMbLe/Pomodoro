from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    sqlite_name: str = 'pomodoro1.sqlite'

