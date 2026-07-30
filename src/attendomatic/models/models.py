from sqlmodel import Field, Session, SQLModel, create_engine, select, UniqueConstraint
from enum import Enum
from datetime import date, datetime, time, timezone


# Defining the DayOfWeek enum to represent days of the week
class DayOfWeek(str, Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


class Status(str, Enum):
    PRESENT = "Present"
    ABSENT = "Absent"
    CANCELLED = "Cancelled"


class Type(str, Enum):
    LECTURE = "Lecture"
    LAB = "Lab"
    TUTORIAL = "Tutorial"


# Defining the User model to represent users in the system
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    uid: str | None = Field(default=None, unique=True)


# Defining the Subject model to represent subjects in the system
class Subject(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    code: str | None = Field(default=None, unique=True)


# Defining the Slot model to represent time slots in the system
class Slot(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    subject_id: int = Field(foreign_key="subject.id")
    type: Type
    day: DayOfWeek
    start_time: time
    end_time: time


# Defining the TimeTable model to represent the association between users and slots
class TimeTable(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    slot_id: int = Field(foreign_key="slot.id")


# Defining the Logs model to represent log entries in the system
class Logs(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "subject_id",
            "type",
            "class_end_time",
            "is_regular",
            "class_date",
            name="unique_log_constraint",
        ),
    )
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    subject_id: int = Field(foreign_key="subject.id")
    type: Type = Field(default=Type.LECTURE)  # Default type is set to LECTURE
    status: Status = Field(default=Status.PRESENT)  # Default status is set to PRESENT
    is_regular: bool = Field(
        default=True
    )  # True = regular timetable class, False = extra class
    class_end_time: time | None = Field(
        default=None
    )  # Optional field for class end time for avoiding duplicate logs in case of extra classes
    class_date: date | None = Field(
        default=None
    )  # Optional field for class date for avoiding duplicate logs in case of extra classes
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
