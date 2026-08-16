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

    def get_subjects_by_user_id(self, user_id: int):
        statement = select(Subject).where(Subject.user_id == user_id)
        return self.session.exec(statement).all()

    def create_subject(self, name: str, code: str):
        subject = Subject(name=name, code=code)
        self.session.add(subject)
        self.session.commit()
        self.session.refresh(subject)
        return subject

    def get_all_subjects(self):
        statement = select(Subject)
        return self.session.exec(statement).all()

    def delete_subject(self, subject_id: int):
        subject = self.get_subject_by_id(subject_id)
        if subject:
            self.session.delete(subject)
            self.session.commit()
            return True
        return False

    def update_subject(
        self, subject_id: int, name: str | None = None, code: str | None = None
    ):
        subject = self.get_subject_by_id(subject_id)
        if subject:
            if name is not None:
                subject.name = name
            if code is not None:
                subject.code = code
            self.session.add(subject)
            self.session.commit()
            self.session.refresh(subject)
            return subject
        return None
