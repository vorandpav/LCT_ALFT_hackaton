import logging
from http.client import HTTPException

from fastapi import APIRouter, HTTPException
from fake_main_server.config import WORKS_IDS
from fake_main_server.services import works

router = APIRouter()

logger = logging.getLogger("works")


@router.get("/")
async def list_works():
    logger.info("Listing all works")
    return WORKS_IDS


@router.get("/{work_id}")
async def get_work(work_id: int):
    if work_id not in WORKS_IDS:
        logger.error(f"Work {work_id} not found")
        raise HTTPException(status_code=404, detail="Work not found")

    logger.info(f"Retrieved work {work_id}: {WORKS_IDS[work_id]}")
    return WORKS_IDS[work_id]


@router.post("/{work_id}/scan_giving")
async def scan_giving(work_id: int):
    logger.info(f"Scanning giving stage for work {work_id}")
    return await works.scan_stage(work_id, stage="giving")


@router.post("/{work_id}/scan_getting")
async def scan_getting(work_id: int):
    logger.info(f"Scanning getting stage for work {work_id}")
    return await works.scan_stage(work_id, stage="getting")


@router.post("/{work_id}/complete_giving")
async def complete_giving(work_id: int):
    logger.info(f"Completing giving stage for work {work_id}")
    return works.complete_stage(work_id, stage="giving")


@router.post("/{work_id}/complete_getting")
async def complete_getting(work_id: int):
    logger.info(f"Completing getting stage for work {work_id}")
    return works.complete_stage(work_id, stage="getting")
