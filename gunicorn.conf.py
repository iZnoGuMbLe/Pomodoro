import os
from dotenv import load_dotenv
from uvicorn.workers import UvicornWorker

bind = "0.0.0.0:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"

environment = os.getenv("ENV")

if environment:
    env_path = os.path.join(os.getcwd(), f".{environment}.env")
    if os.path.exists(env_path):
        load_dotenv(env_path)