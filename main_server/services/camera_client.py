import logging
import re

import httpx
from fastapi import HTTPException

from main_server.config import FAKE_CAMERA_URL

logger = logging.getLogger("camera_client")


async def get_photo(work_id: int) -> tuple[bytes, str | None]:
    """Получает фото из сервиса камеры и возвращает его как байты и имя файла."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(f"{FAKE_CAMERA_URL}/{work_id}")
            response.raise_for_status()
            filename = None
            content_disposition = response.headers.get("content-disposition")
            if content_disposition:
                match = re.search(r'filename="?([^"]+)"?', content_disposition)
                if match:
                    filename = match.group(1)
            logger.info(f"Received photo for work_id={work_id}. Filename: {filename}")
            return response.content, filename

        except httpx.TimeoutException:
            logger.error(f"Timeout when taking photo for work_id={work_id}")
            raise HTTPException(status_code=504, detail="Camera service timeout")
        except httpx.HTTPError as e:
            print(e)
            logger.error(f"Failed to take photo for work_id={work_id}, error: {str(e)}")
            raise HTTPException(status_code=502, detail="Camera service error")
