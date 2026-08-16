from sqlmodel import Session, select

from attendomatic.models.models import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_id(self, user_id: int):
        return self.session.get(User, user_id)

    def get_user_by_email(self, email: str):
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def get_user_by_uid(self, uid: str):
        statement = select(User).where(User.uid == uid)
        return self.session.exec(statement).first()
