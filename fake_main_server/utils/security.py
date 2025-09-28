from fastapi import HTTPException
from config import TEST_USERS, WORKS_IDS


def check_access(user_id: int, work_id: int):
    if user_id not in TEST_USERS:
        raise HTTPException(status_code=404, detail="User not found")
    if work_id not in WORKS_IDS:
        raise HTTPException(status_code=404, detail="Work not found")

    user = TEST_USERS[user_id]
    work = WORKS_IDS[work_id]

    if user["powers"] == "admin":
        return True
    if user["powers"] == "technician" and work["user_id"] == user["user_id"]:
        return True

    raise HTTPException(status_code=403, detail="Access denied")
