from fastapi import FastAPI
from . import config
from functools import lru_cache

app = FastAPI()


@lru_cache()
def get_settings():
    return config.Settings()


@app.on_event("startup")
async def startup_event():
    from .models.main import create_db_and_tables

    create_db_and_tables()


@app.get("/")
async def read_root():
    return {"message": "Welcome to Attendomatic!", "app_name": get_settings().app_name}
