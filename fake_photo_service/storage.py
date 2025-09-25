import os
import logging
from fastapi.responses import FileResponse
from fastapi import HTTPException
from .config import PHOTO_BASE_DIR, TEST_RESPONSES

log = logging.getLogger(__name__)

current_index = {}


def get_photo_path(table_id: str, step: int | None = None):
    """Определяет путь к файлу фото для указанного table_id и шага"""
    if table_id not in TEST_RESPONSES:
        raise HTTPException(status_code=404, detail="table_id not found")

    photos = TEST_RESPONSES[table_id]

    if step is not None:
        idx = step - 1
    else:
        idx = current_index.get(table_id, 0)
        current_index[table_id] = idx + 1

    if idx < 0 or idx >= len(photos):
        raise HTTPException(status_code=404, detail="No photo for this step")

    photo_path = os.path.join(PHOTO_BASE_DIR, photos[idx])
    if not os.path.exists(photo_path):
        log.error(f"File not found: {photo_path}")
        raise HTTPException(status_code=500, detail=f"File not found: {photos[idx]}")

    return photo_path


def serve_photo(photo_path: str) -> FileResponse:
    """Отдаёт файл как HTTP-ответ"""
    return FileResponse(photo_path, media_type="image/jpeg")
