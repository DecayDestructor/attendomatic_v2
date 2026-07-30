from sqlmodel import Session, select
from ..models.models import Subject


class SubjectRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_subject_by_id(self, subject_id: int):
        return self.session.get(Subject, subject_id)

    def get_subject_by_code(self, code: str):
        statement = select(Subject).where(Subject.code == code)
        return self.session.exec(statement).first()

    def create_subject(self, name: str, code: str):
        subject = Subject(name=name, code=code)
        self.session.add(subject)
        self.session.commit()
        self.session.refresh(subject)
        return subject
