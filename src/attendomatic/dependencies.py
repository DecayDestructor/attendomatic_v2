def get_session():
    from sqlmodel import Session
    from .models.main import get_engine

    engine = get_engine()
    with Session(engine) as session:
        yield session
