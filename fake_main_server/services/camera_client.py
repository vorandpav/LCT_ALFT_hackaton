import logging
from http.client import HTTPException
import httpx

FAKE_CAMERA_URL = "http://localhost:8001"

logger = logging.getLogger("camera_client")


async def get_photo(work_id: int):
    async with httpx.AsyncClient() as client:
        logger.info(f"Requesting photo for work_id {work_id} from camera service")
        resp = await client.get(f"{FAKE_CAMERA_URL}/table_id", params={"table_id": work_id})
        logger.info(f"Camera service responded with status code {resp.status_code} for work_id {work_id}")
        resp.raise_for_status()
        return resp.json()
