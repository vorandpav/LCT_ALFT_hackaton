from fastapi import HTTPException

from main_server.config import USERS_IDS, WORK_STAGES, WORKS_IDS


def check_access(user_id: int, work_id: int):
    if user_id not in USERS_IDS:
        raise HTTPException(status_code=404, detail="User not found")
    if work_id not in WORKS_IDS:
        raise HTTPException(status_code=404, detail="Work not found")

    user = USERS_IDS[user_id]
    work = WORKS_IDS[work_id]

    if user["powers"] == "admin":
        return True
    if user["powers"] == "technician" and work["user_id"] == user_id:
        return True

    raise HTTPException(status_code=403, detail="Access denied")


def check_correctness(user_id: int = None, work_id: int = None, stage: str = None):
    if user_id is not None:
        if user_id not in USERS_IDS:
            print(USERS_IDS)
            raise HTTPException(status_code=404, detail="User not found")

    if work_id is not None:
        if work_id not in WORKS_IDS:
            raise HTTPException(status_code=404, detail="Work not found")

    if stage is not None:
        if stage not in WORK_STAGES:
            raise HTTPException(status_code=400, detail="Invalid stage")

    if work_id is not None and stage is not None:
        work = WORKS_IDS[work_id]
        if work["stage"] != stage:
            raise HTTPException(
                status_code=400, detail="Stage does not match work's current stage"
            )
    return True
