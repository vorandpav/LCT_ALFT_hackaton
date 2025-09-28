import logging
from config import WORKS_IDS
from services import camera_client, cv_client
from utils import photos, mapping

log = logging.getLogger(__name__)


async def scan_stage(work_id: int, stage: str):
    # получаем фото с камеры
    photo = await camera_client.get_photo(work_id)
    # прогоняем через CV
    detections = await cv_client.infer(photo)

    # сохраняем фото и результаты
    photo_id = photos.generate_id(work_id, stage)
    WORKS_IDS[work_id][f"photo_ids_{stage}"] = photo_id
    WORKS_IDS[work_id][f"boxes_{stage}"] = detections["detections"]

    log.info(f"Saved photo {photo_id} for work {work_id}, stage={stage}")
    return detections


def complete_stage(work_id: int, stage: str):
    # простая проверка — есть ли вообще фото
    if not WORKS_IDS[work_id][f"photo_ids_{stage}"]:
        return {"error": "No photos scanned"}
    WORKS_IDS[work_id]["state"] = "in_work" if stage == "giving" else "completed"
    return {"status": "ok", "state": WORKS_IDS[work_id]["state"]}
