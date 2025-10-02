import logging

import httpx
from fastapi import HTTPException

from fake_main_server.config import FAKE_CV_URL

logger = logging.getLogger("cv_client")


async def infer(photo_bytes: bytes):
    """Отправляет байты фото в CV-сервис для распознавания."""
    files = {"file": ("photo.jpg", photo_bytes, "image/jpeg")}
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            response = await client.post(f"{FAKE_CV_URL}/infer", files=files)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"CV inference failed: {e.text}")
            raise HTTPException(status_code=502, detail="CV service error")
