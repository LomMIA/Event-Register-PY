from datetime import datetime, timezone

from fastapi import Depends, FastAPI, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .db import get_session
from .models import Event
from .schemas import EventOut

app = FastAPI(title='Events API')


@app.get('/api/events', response_model=list[EventOut])
async def list_events(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    q: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    query = (
        select(Event)
        .where(Event.status == 'published', Event.starts_at > datetime.now(timezone.utc))
        .order_by(Event.starts_at)
    )

    if q:
        query = query.where(Event.name.ilike(f'%{q}%'))

    query = query.limit(limit).offset(offset)

    result = await session.scalars(query)
    return result.all()