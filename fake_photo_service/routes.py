import asyncio
import logging
from fastapi import APIRouter
from .storage import get_photo_path, serve_photo

router = APIRouter()
log = logging.getLogger(__name__)


@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "Fake Photo Service is running"}


@router.get("/photos/{table_id}")
async def get_photo(table_id: str, step: int | None = None):
    """
    Возвращает фото для заданного table_id.
    - ?step=N → фото для конкретного шага
    - без step → выдаёт следующее фото по порядку
    """
    await asyncio.sleep(1)
    photo_path = get_photo_path(table_id, step)
    log.info(f"Serving {photo_path} for table_id={table_id}, step={step}")
    return serve_photo(photo_path)
