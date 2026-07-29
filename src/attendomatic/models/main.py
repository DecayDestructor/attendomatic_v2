from sqlmodel import SQLModel, Session, create_engine
from ..config import get_settings
from .models import User, Subject, Slot, TimeTable

engine = create_engine(get_settings().database_url)


def create_db_and_tables():
    print("Known tables:", SQLModel.metadata.tables.keys())

    SQLModel.metadata.create_all(engine)

    print("Database and tables created successfully.")


def get_engine():
    return engine
