import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = 'events_event'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    location: Mapped[str]
    capacity: Mapped[int]
    status: Mapped[str]
    organizer_id: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class Registration(Base):
    __tablename__ = 'events_registration'

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey('events_event.id'))
    name: Mapped[str]
    email: Mapped[str]
    ticket_code: Mapped[uuid.UUID]
    status: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))