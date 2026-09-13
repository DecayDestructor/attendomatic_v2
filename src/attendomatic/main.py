from fastapi import FastAPI
from . import config
from fastmcp import FastMCP

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    from .models.main import create_db_and_tables

    create_db_and_tables()


@app.get("/")
async def read_root():
    return {
        "message": "Welcome to Attendomatic!",
        "app_name": config.get_settings().app_name,
    }
