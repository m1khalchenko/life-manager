from typing import List

from fastapi import APIRouter, HTTPException

from rest.models import Timer
from rest.schemas import TimerSchema
from rest.factories import TimerFactory
from rest.schemas.timer import CreateTimerSchema

router = APIRouter(tags=["timer"])

@router.post('/timers')
async def create_timer(data: CreateTimerSchema) -> TimerSchema:
    timer = await TimerFactory(
        data_for_create=data
    ).create()
    return timer

@router.get('/timers')
async def create_timer() -> List[TimerSchema]:
    timers = await Timer.get_objects()
    return timers


@router.get('/timer/{timer_id}')
async def create_timer(timer_id: int) -> TimerSchema:
    timer = await Timer.get_object(timer_id)

    if timer is None:
        raise HTTPException(status_code=404, detail="Timer not found")

    return timer


@router.delete('/timer/{timer_id}')
async def create_timer(timer_id: int) -> None:
    await Timer.delete_object(timer_id)
