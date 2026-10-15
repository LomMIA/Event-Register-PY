from datetime import datetime, timezone

from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .db import get_session
from .models import Event
from .schemas import EventOut

app = FastAPI(title='Events API')


@app.get('/api/events', response_model=list[EventOut])
async def list_events(session: AsyncSession = Depends(get_session)):
    query = select(Event).where(Event.status == 'published', Event.starts_at > datetime.now(timezone.utc)).order_by(Event.starts_at)
    result = await session.scalars(query)
    return result.all()