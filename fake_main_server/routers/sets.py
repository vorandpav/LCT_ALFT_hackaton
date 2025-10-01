import logging

from fastapi import APIRouter, HTTPException

from fake_main_server.config import TOOLS_IDS, TOOLS_SETS_IDS

router = APIRouter()

logger = logging.getLogger("sets")


@router.get("/")
async def list_sets():
    logger.info("Listing all tool sets")
    return TOOLS_SETS_IDS


@router.get("/{set_id}")
async def get_set(set_id: int):
    if set_id not in TOOLS_SETS_IDS:
        logger.error(f"Set {set_id} not found")
        raise HTTPException(404, "Set not found")

    tools = [TOOLS_IDS[t] for t in TOOLS_SETS_IDS[set_id]["tools"]]
    logger.info(f"Retrieved set {set_id} with tools: {tools}")
    return {"set": TOOLS_SETS_IDS[set_id], "tools": tools}
