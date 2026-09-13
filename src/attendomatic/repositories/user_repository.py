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

    def create_user(self, name: str, email: str, uid: str, is_admin: bool = False):
        new_user = User(name=name, email=email, uid=uid, is_admin=is_admin)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user
