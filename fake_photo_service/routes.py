import asyncio
import logging
import os

from fastapi import APIRouter

from .storage import get_photo_path, serve_photo

router = APIRouter()
log = logging.getLogger("fake_photo_service")


@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "Fake Photo Service is running"}


@router.get("/{work_id}")
async def get_photo(work_id: str):
    await asyncio.sleep(1)
    photo_path = get_photo_path(work_id)
    log.info(f"Serving {photo_path} for work_id={work_id}")
    return serve_photo(photo_path)
