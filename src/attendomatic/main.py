from fastapi import FastAPI
from . import config
from functools import lru_cache
from fastmcp import FastMCP

app = FastAPI()

mcp = FastMCP.from_fastapi(app=app)


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


if __name__ == "__main__":
    mcp.run()
