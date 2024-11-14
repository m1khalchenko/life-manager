from typing import List

from fastapi import (
    APIRouter,
    HTTPException,
)
from rest.factories import TimerFactory
from rest.models import Timer
from rest.schemas import TimerSchema
from rest.schemas.timer import (
    CreateTimerSchema,
    UpdateTimerSchema,
)
from rest.utils.helpers.timer.timer_update import TimerUpdate

router = APIRouter(tags=["timer"])


@router.post('/timers', response_model=TimerSchema)
async def create_timer(data: CreateTimerSchema) -> Timer:
    obj = await TimerFactory(
        data_for_create=data.model_dump(),
    ).create()
    timer = await Timer.get_object(obj.id)  # type: ignore
    return timer


@router.get('/timers', response_model=List[TimerSchema])
async def get_timers() -> List[Timer]:
    timers = await Timer.get_objects()
    return timers


@router.get('/timer/{timer_id}', response_model=TimerSchema)
async def get_timer(timer_id: int) -> Timer:
    timer = await Timer.get_object(timer_id)

    if timer is None:
        raise HTTPException(status_code=404, detail="Timer not found")

    return timer


@router.delete('/timer/{timer_id}')
async def delete_timer(timer_id: int) -> None:
    await Timer.delete_object(timer_id)


@router.patch('/timer/{timer_id}', response_model=TimerSchema)
async def update_timer(timer_id: int, data: UpdateTimerSchema) -> Timer:
    timer = await Timer.get_object(timer_id)

    resp: Timer = await TimerUpdate(
        data_for_update=data.model_dump(),
        instance=timer,
    ).update()

    return resp
