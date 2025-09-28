import logging
import httpx
from fastapi import HTTPException

from fake_main_server.config import FAKE_CAMERA_URL

logger = logging.getLogger("camera_client")


async def get_photo(work_id: int):
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(f"{FAKE_CAMERA_URL}/{work_id}")
            response.raise_for_status()
        except httpx.TimeoutException:
            logger.error(f"Timeout when taking photo for work_id={work_id}")
            raise HTTPException(status_code=504, detail="Camera service timeout")
        except httpx.HTTPError as e:
            logger.error(f"Failed to take photo for work_id={work_id}, error: {e}")
            raise HTTPException(status_code=502, detail="Camera service error")

    logger.info(f"Photo taken for work_id={work_id}")
    return response.json()
