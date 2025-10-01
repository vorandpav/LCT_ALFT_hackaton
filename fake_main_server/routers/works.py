import logging
from http.client import HTTPException

from fastapi import APIRouter, HTTPException

from fake_main_server.config import WORKS_IDS
from fake_main_server.services import works
from fake_main_server.utils import security

router = APIRouter()

logger = logging.getLogger("works")


@router.get("/")
async def list_works():
    logger.info("Listing all works")
    return WORKS_IDS


@router.get("/{work_id}/{stage}")
async def upload_data(work_id: int, stage: str):
    if stage not in ["GIVING", "GETTING"]:
        logger.error(f"Invalid stage {stage} for work {work_id}")
        raise HTTPException(400, "Invalid stage")
    try:
        security.check_correctness(work_id=work_id, stage=stage)
    except HTTPException as e:
        logger.error(f"Approval failed for work {work_id} at stage {stage}: {e}")
        raise e

    logger.info(f"Retrieved work {work_id} at stage {stage}")
    return await works.upload_data(work_id, stage)


@router.get("/{work_id}/{stage}/report")
async def upload_report(work_id: int, stage: str):
    try:
        security.check_correctness(work_id=work_id, stage=stage)
    except HTTPException as e:
        logger.error(f"Approval failed for work {work_id} at stage {stage}: {e}")
        raise e

    logger.info(f"Retrieved work {work_id} at stage {stage}")
    return await works.upload_data(work_id, "REPORT")


@router.post("/{work_id}/{stage}/scan")
async def scan_table(work_id: int, stage: str):
    try:
        security.check_correctness(work_id=work_id, stage=stage)
    except HTTPException as e:
        logger.error(f"Approval failed for work {work_id} at stage {stage}: {e}")
        raise e

    logger.info(f"Scanning at {stage} for work {work_id}")
    return await works.scan_table(work_id, stage)


@router.post("/{work_id}/{stage}/approve")
async def approve_box(work_id: int, stage: str, box: dict):
    try:
        security.check_correctness(work_id=work_id, stage=stage)
    except HTTPException as e:
        logger.error(f"Approval failed for work {work_id} at stage {stage}: {e}")
        raise e

    logger.info(f"Approving box at {stage} for work {work_id}: {box}")
    return await works.approve_box(work_id, stage=stage, box=box)


@router.post("/{work_id}/{stage}/complete")
async def complete_stage(work_id: int, stage: str):
    try:
        security.check_correctness(work_id=work_id, stage=stage)
    except HTTPException as e:
        logger.error(f"Approval failed for work {work_id} at stage {stage}: {e}")
        raise e

    logger.info(f"Completing stage {stage} for work {work_id}")
    return await works.complete_stage(work_id)


@router.post("/{work_id}/{stage}/error")
async def error_stage(work_id: int, stage: str):
    try:
        security.check_correctness(work_id=work_id, stage=stage)
    except HTTPException as e:
        logger.error(f"Error reporting failed for work {work_id} at stage {stage}: {e}")
        raise e

    logger.info(f"Reporting error at stage {stage} for work {work_id}")
    return await works.error_stage(work_id)
