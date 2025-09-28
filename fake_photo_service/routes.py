import asyncio
import logging
from fastapi import APIRouter
from .storage import get_photo_path, serve_photo

router = APIRouter()
log = logging.getLogger(__name__)


@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "Fake Photo Service is running"}


@router.get("/photos/{work_id}")
async def get_photo(work_id: str, step: int | None = None):
    """
    Возвращает фото для заданного work_id.
    - ?step=N → фото для конкретного шага
    - без step → выдаёт следующее фото по порядку
    """
    await asyncio.sleep(1)
    photo_path = get_photo_path(work_id, step)
    log.info(f"Serving {photo_path} for work_id={work_id}, step={step}")
    return serve_photo(photo_path)
