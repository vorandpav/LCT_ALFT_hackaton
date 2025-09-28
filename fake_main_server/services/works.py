import logging
from fake_main_server.config import WORKS_IDS, TOOLS_SETS_IDS, WORK_STAGES
from fake_main_server.services import camera_client, cv_client
from fake_main_server.utils import photos, mapping
import httpx
from fastapi import HTTPException

log = logging.getLogger(__name__)


async def scan_table(work_id: int, stage: str):
    """Одно сканирование"""

    photo = await camera_client.get_photo(work_id)
    detections = await cv_client.infer(photo)

    # сохраняем фото
    photo_name = photos.generate_id(work_id, stage)
    WORKS_IDS[work_id][f"photo_ids_{stage}"].append(photo_name)
    try:
        photos.save(photo, photo_name)
    except Exception as e:
        log.error(f"Failed to save photo {photo_name} for work {work_id}, error: {e}")
        return {"error": "Failed to save photo"}

    # сводим боксы к нужному формату
    boxes = []
    for det in detections:
        mapped_name = mapping.map_tool_class_to_names(
            det["predicted_class"],
            WORKS_IDS[work_id]["tools_set_id"]
        )
        boxes.append({
            "bbox": det["bbox"],
            "predicted_name": mapped_name,
            "confidence": det["confidence"]})

    log.info(f"Scanned photo {photo_name} for work {work_id}, stage={stage}, detections: {boxes}")
    return {"photo_name": photo_name, "photo": photo, "boxes": boxes}


async def approve_box(work_id: int, stage: str, box: dict):
    """Подтверждение инструмента в боксе"""
    WORKS_IDS[work_id][f"boxes_{stage}"].append(box)
    WORKS_IDS[work_id][f"detected_tools_{stage}"].append(box["approved_id"])
    log.info(f"Approved box {box} for work {work_id}, stage={stage}")
    return {"status": "ok"}


async def upload_data(work_id: int, stage: str):
    """Загрузка всех данных по работе на данном этапе"""
    photo_ids = WORKS_IDS[work_id][f"photo_ids_{stage}"]
    photo_data = [{
        "photo_id": pid,
        "photo": photos.load(pid)
    } for pid in photo_ids]
    boxes = WORKS_IDS[work_id][f"boxes_{stage}"]
    detected_tools = WORKS_IDS[work_id][f"detected_tools_{stage}"]

    data = {
        "photos": photo_data,
        "boxes": boxes,
        "detected_tools": detected_tools,
    }

    return data


def complete_stage(work_id: int, stage: str):
    """Завершение этапа работы"""
    if stage == "COMPLETED":
        log.error("Cannot complete stage 'COMPLETED'")
        raise HTTPException(status_code=400, detail="Cannot complete stage 'COMPLETED'")
    if (stage in ["GIVING", "GETTING"]
            and len(WORKS_IDS[work_id][f"detected_tools_{stage}"]) < len(
                TOOLS_SETS_IDS[WORKS_IDS[work_id]["tools_set_id"]]["tools"])):
        log.warning(f"Cannot complete stage {stage} for work {work_id}, not all tools detected")
        return {"error": "Not all tools detected"}
    WORKS_IDS[work_id]["stage"] = WORK_STAGES[WORK_STAGES.index(stage) + 1]
    log.info(f"Completed stage {stage} for work {work_id}, new stage: {WORKS_IDS[work_id]['stage']}")
    return {"new_stage": WORKS_IDS[work_id]["stage"]}
