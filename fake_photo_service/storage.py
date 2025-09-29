import os
import logging
from fastapi.responses import FileResponse
from fastapi import HTTPException
from .config import PHOTO_BASE_DIR, TEST_RESPONSES

log = logging.getLogger("fake_photo_service")

current_index = {}


def get_photo_path(work_id: str):
    """Определяет путь к файлу фото для указанного work_id"""
    if work_id not in TEST_RESPONSES:
        raise HTTPException(status_code=404, detail="work_id not found")

    photos = TEST_RESPONSES[work_id]

    idx = current_index.get(work_id, 0)
    current_index[work_id] = idx + 1

    if idx < 0 or idx >= len(photos):
        raise HTTPException(status_code=404, detail="No photo for this step")

    photo_path = f"{PHOTO_BASE_DIR}/{photos[idx]}"
    if not os.path.exists(photo_path):
        log.error(f"File not found: {photo_path}")
        raise HTTPException(status_code=500, detail=f"File not found: {photos[idx]}")

    return photo_path


def serve_photo(photo_path: str) -> FileResponse:
    """Отдаёт файл как HTTP-ответ"""
    return FileResponse(photo_path, media_type="image/jpeg")
