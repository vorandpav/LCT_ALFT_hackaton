import logging
import httpx
from fastapi import HTTPException

FAKE_CV_URL = "http://localhost:9001"

logger = logging.getLogger("cv_client")


async def infer(photo: dict):
    files = {"file": ("photo.jpg", bytes.fromhex(photo["photo_data"]), "image/jpeg")}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{FAKE_CV_URL}/infer", files=files)
            response.raise_for_status()
        except httpx.HTTPError as e:
            logger.error(f"CV inference failed: {e}")
            raise HTTPException(status_code=502, detail="CV service error")
    logger.info("CV inference successful")
    return response.json()
