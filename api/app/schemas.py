from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    starts_at: datetime
    location: str
    capacity: int


class EventDetailOut(EventOut):
    free_places: int
