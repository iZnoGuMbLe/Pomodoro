from typing import Union

from fastapi import FastAPI
from handlers import routers

app = FastAPI()

for rounter in routers:
    app.include_router(rounter)
