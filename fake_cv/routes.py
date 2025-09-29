import asyncio
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from .storage import find_matching_file, load_result

router = APIRouter()
log = logging.getLogger(__name__)


@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "Fake CV Service is running"}


@router.post("/infer")
async def infer(file: UploadFile = File(...)):
    """Принимает фото и возвращает заранее подготовленный результат"""
    await asyncio.sleep(2)

    content = await file.read()
    match = find_matching_file(content)

    if not match:
        log.warning("No match for uploaded file")
        raise HTTPException(status_code=404, detail="No match for uploaded file")

    log.info(f"Matched file: {match}")
    result = load_result(match)
    return JSONResponse(content=result)
