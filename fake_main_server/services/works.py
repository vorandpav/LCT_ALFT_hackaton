import base64
import logging
from fake_main_server.config import WORKS_IDS, TOOLS_SETS_IDS, WORK_STAGES, TOOLS_IDS
from fake_main_server.services import camera_client, cv_client
from fake_main_server.utils import photos, mapping
import httpx
from fastapi import HTTPException

logger = logging.getLogger(__name__)


async def scan_table(work_id: str, stage: str):
    """Один цикл сканирования: получить фото, распознать, сохранить."""
    try:
        # 1. Получаем фото как байты
        photo_bytes = await camera_client.get_photo(work_id)
        logger.info(f"Captured photo for work {work_id}, stage={stage} ({len(photo_bytes)} bytes)")

        # 2. Отправляем байты в CV-сервис
        cv_answer = await cv_client.infer(photo_bytes)
        logger.info(f"Received {len(cv_answer)} detections from CV for work {work_id}, stage={stage}")

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error during scanning for work {work_id}, stage={stage}: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error during scanning")

    # 3. Генерируем ID и сохраняем фото, используя ваш модуль
    photo_name = photos.generate_id(work_id, stage)
    try:
        # Используем функцию save из модуля photos
        photos.save(photo_bytes, photo_name)
        WORKS_IDS[work_id][f"photo_ids_{stage}"].append(photo_name)
        logger.info(f"Photo saved as {photo_name}")
    except ValueError as e:
        # Обрабатываем ошибки валидации или существования файла от модуля photos
        logger.error(f"Failed to save photo {photo_name} for work {work_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurred while saving photo {photo_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to save photo")

    # 4. Обрабатываем результат
    boxes = []
    for det in cv_answer["detections"]:
        boxes.append({
            "bbox": det["bbox"],
            "predicted_name": det["predicted_class"],
            "confidence": det["confidence"]
        })

    logger.info(f"Scanned photo {photo_name} for work {work_id}, stage={stage}, detections: {boxes}")

    photo_base64 = base64.b64encode(photo_bytes).decode('utf-8')

    return {
        "photo_name": photo_name,
        "advice": cv_answer["advice"],
        "photo_base64": photo_base64,
        "boxes": boxes
    }


async def approve_box(work_id: int, stage: str, box: dict):
    """Подтверждение инструмента в боксе"""
    WORKS_IDS[work_id][f"approved_boxes_{stage}"].append(box)
    logger.info(f"Approved box {box} for work {work_id}, stage={stage}")
    return {"status": "ok"}


async def upload_data(work_id: int, stage: str):
    """Загрузка всех данных по работе на данном этапе"""
    data = {
        "tid_to_tname": {},
        "tname_to_tid": {},

    }
    tools_to_be_approved = set(TOOLS_SETS_IDS[WORKS_IDS[work_id]["set_id"]]["tools"])

    if stage in ["GIVING", "GETTING"]:
        photo_ids = WORKS_IDS[work_id][f"photo_ids_{stage}"]
        photo_data = [{
            "photo_id": pid,
            "photo": photos.load(pid)
        } for pid in photo_ids]
        approved_boxes = WORKS_IDS[work_id][f"approved_boxes_{stage}"]
        tools_to_be_approved -= set([box["approved_id"] for box in approved_boxes])

        data.update({
            "photo_data": photo_data,
            "approved_boxes": approved_boxes,
        })

    for tid in tools_to_be_approved:
        tool_name = TOOLS_IDS[tid]
        data["tid_to_tname"][tid] = tool_name
        if tool_name not in data["tname_to_tid"]:
            data["tname_to_tid"][tool_name] = []
        data["tname_to_tid"][tool_name].append(tid)

    return data


async def complete_stage(work_id: int, stage: str):
    """Завершение этапа работы"""
    if stage == "COMPLETED":
        logger.error("Cannot complete stage 'COMPLETED'")
        raise HTTPException(status_code=400, detail="Cannot complete stage 'COMPLETED'")
    if (stage in ["GIVING", "GETTING"]
            and len(WORKS_IDS[work_id][f"approved_boxes_{stage}"]) < len(
                TOOLS_SETS_IDS[WORKS_IDS[work_id]["set_id"]]["tools"])):
        logger.warning(f"Cannot complete stage {stage} for work {work_id}, not all tools detected")
        return {"error": "Not all tools detected"}
    WORKS_IDS[work_id]["stage"] = WORK_STAGES[WORK_STAGES.index(stage) + 1]
    logger.info(f"Completed stage {stage} for work {work_id}, new stage: {WORKS_IDS[work_id]['stage']}")
    return {"new_stage": WORKS_IDS[work_id]["stage"]}
