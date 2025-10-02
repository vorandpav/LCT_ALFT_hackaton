import logging

from fastapi import APIRouter, HTTPException

from main_server.config import USERS_IDS, WORKS_IDS
from main_server.utils import security

router = APIRouter()

logger = logging.getLogger("users")


@router.get("/")
async def list_users():
    logger.info("Listing all users")
    return USERS_IDS


@router.get("/{user_id}")
async def get_user(user_id: int):
    if user_id not in USERS_IDS:
        logger.error(f"User {user_id} not found")
        raise HTTPException(404, "User not found")

    logger.info(f"Retrieved user {user_id}: {USERS_IDS[user_id]}")
    return USERS_IDS[user_id]


@router.get("/authorize/{user_id}/work/{work_id}")
async def authorize_user(user_id: int, work_id: int):
    """Проверка прав пользователя на работу"""
    try:
        security.check_correctness(user_id=user_id)
        security.check_access(user_id, work_id)
    except HTTPException as e:
        logger.error(f"Authorization failed for user {user_id} on work {work_id}: {e}")
        raise e

    logger.info(f"User {user_id} authorized for work {work_id}")
    return {
        "user_name": USERS_IDS[user_id]["user_name"],
        "powers": USERS_IDS[user_id]["powers"],
        "stage": WORKS_IDS[work_id]["stage"],
    }
