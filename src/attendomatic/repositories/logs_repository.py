from sqlmodel import Session, select
from ..models.models import Logs, DayOfWeek, Status, Type
from datetime import date, datetime


class LogsRepository:
    def __init__(self, session: Session):
        self.session = session

    def _build_query(
        self,
        user_id: int | None = None,
        subject_id: int | None = None,
        type: Type | None = None,
        status: Status | None = None,
        is_regular: bool | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ):
        statement = select(Logs)

        if user_id is not None:
            statement = statement.where(Logs.user_id == user_id)

        if subject_id is not None:
            statement = statement.where(Logs.subject_id == subject_id)

        if type is not None:
            statement = statement.where(Logs.type == type)

        if status is not None:
            statement = statement.where(Logs.status == status)

        if is_regular is not None:
            statement = statement.where(Logs.is_regular == is_regular)

        if start_date is not None:
            statement = statement.where(Logs.class_date >= start_date)

        if end_date is not None:
            statement = statement.where(Logs.class_date <= end_date)

        return statement

    def create_log(self, log: Logs):
        self.session.add(log)
        self.session.commit()
        self.session.refresh(log)
        return log

    def update_log(self, log: Logs):

        self.session.add(log)
        self.session.commit()
        self.session.refresh(log)
        return log

    def delete_log(self, log: Logs):
        self.session.delete(log)
        self.session.commit()

    def get_logs(
        self,
        user_id: int | None = None,
        subject_id: int | None = None,
        type: Type | None = None,
        status: Status | None = None,
        isRegular: bool | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ):
        statement = self._build_query(
            user_id=user_id,
            subject_id=subject_id,
            type=type,
            status=status,
            is_regular=isRegular,
            start_date=start_date,
            end_date=end_date,
        )
        return self.session.exec(statement).all()

    def get_log(
        self,
        user_id: int | None = None,
        subject_id: int | None = None,
        type: Type | None = None,
        status: Status | None = None,
        is_regular: bool | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ):
        statement = self._build_query(
            user_id=user_id,
            subject_id=subject_id,
            type=type,
            status=status,
            is_regular=is_regular,
            start_date=start_date,
            end_date=end_date,
        )
        return self.session.exec(statement).first()
