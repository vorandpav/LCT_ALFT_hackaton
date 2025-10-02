import base64
import logging

from fastapi import HTTPException

from main_server.config import (TOOLS_IDS, TOOLS_SETS_IDS, WORK_STAGES,
                                     WORKS_IDS)
from main_server.services import camera_client, cv_client
from main_server.utils import mapping, photos

logger = logging.getLogger(__name__)


async def scan_table(work_id: int, stage: str):
    """Один цикл сканирования: получить фото, распознать, сохранить."""
    try:
        photo_bytes, filename = await camera_client.get_photo(work_id)
        logger.info(
            f"Captured photo for work {work_id}, stage={stage} ({len(photo_bytes)} bytes)"
        )
        cv_answer = await cv_client.infer(photo_bytes)
        logger.info(
            f"Received {len(cv_answer)} detections from CV for work {work_id}, stage={stage}"
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(
            f"Unexpected error during scanning for work {work_id}, stage={stage}: {e}"
        )
        raise HTTPException(status_code=500, detail="Unexpected error during scanning")

    # photo_id = photos.generate_id(work_id, stage)
    try:
        # photos.save(photo_bytes, photo_id)
        WORKS_IDS[work_id][f"photo_ids_{stage}"].append(filename)
        logger.info(f"Photo saved as {filename}")
    except ValueError as e:
        logger.error(f"Failed to save photo {filename} for work {work_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurred while saving photo {filename}: {e}")
        raise HTTPException(status_code=500, detail="Failed to save photo")

    boxes = []

    tools_to_be_approved = set(TOOLS_SETS_IDS[WORKS_IDS[work_id]["set_id"]]["tools"])
    approved_boxes = WORKS_IDS[work_id][f"approved_boxes_{stage}"]
    tools_to_be_approved -= set([box["tool_id"] for box in approved_boxes])

    try:
        for det in cv_answer["detections"]:
            mapped_tool = mapping.map_tool_class_to_names(
                det["predicted_class"], tools_to_be_approved
            )
            if not mapped_tool:
                continue
            boxes.append(
                {
                    "bbox": det["bbox"],
                    "predicted_name": mapped_tool,
                    "confidence": det["confidence"],
                }
            )
    except ValueError as e:
        logger.error(f"Mapping error for work {work_id}, stage={stage}: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    logger.info(
        f"Scanned photo {filename} for work {work_id}, stage={stage}, detections: {boxes}"
    )

    photo_base64 = base64.b64encode(photo_bytes).decode("utf-8")

    return {
        "photo_id": filename,
        "photo_base64": photo_base64,
        "boxes": boxes,
    }


async def approve_box(work_id: int, stage: str, box: dict):
    """Подтверждение инструмента в боксе"""
    WORKS_IDS[work_id][f"approved_boxes_{stage}"].append(box)
    logger.info(f"Approved box {box} for work {work_id}, stage={stage}")
    return {"status": "ok"}


async def upload_data(work_id: int, stage: str):
    """Загрузка всех данных по работе на данном этапе"""
    all_tools = set(TOOLS_SETS_IDS[WORKS_IDS[work_id]["set_id"]]["tools"])

    def process_stored_data(processing_stage: str, all_tools: set):
        photo_ids = WORKS_IDS[work_id][f"photo_ids_{processing_stage}"]
        photo_data = [
            {"photo_id": pid, "photo_base64": photos.load_base64(pid)}
            for pid in photo_ids
        ]
        approved_boxes = WORKS_IDS[work_id][f"approved_boxes_{processing_stage}"]
        approved_boxes = [
            box.update({"tool_name": TOOLS_IDS[box["tool_id"]]}) or box
            for box in approved_boxes
        ]

        tools_to_be_approved = all_tools - set([box["tool_id"] for box in approved_boxes])

        return {
            "tid_to_tname": {tid: TOOLS_IDS[tid] for tid in tools_to_be_approved},
            "photo_data": photo_data,
            "approved_boxes": approved_boxes,
        }

    if stage in ["GIVING", "GETTING"]:
        return process_stored_data(stage, all_tools)
    else:
        return {
            "GIVING": process_stored_data("GIVING", all_tools),
            "GETTING": process_stored_data("GETTING", all_tools),
        }


async def complete_stage(work_id: int):
    """Завершение этапа работы"""
    stage = WORKS_IDS[work_id]["stage"]
    if stage in ["COMPLETED", "ERROR"]:
        logger.error(f"Cannot complete stage {stage}")
        raise HTTPException(status_code=400, detail=f"Cannot complete stage {stage}")

    if stage in ["GIVING", "GETTING"] and len(
            WORKS_IDS[work_id][f"approved_boxes_{stage}"]
    ) < len(TOOLS_SETS_IDS[WORKS_IDS[work_id]["set_id"]]["tools"]):
        logger.warning(
            f"Cannot complete stage {stage} for work {work_id}, not all tools detected"
        )
        return {"ok": False, "error": "Not all tools detected"}

    WORKS_IDS[work_id]["stage"] = WORK_STAGES[WORK_STAGES.index(stage) + 1]
    logger.info(
        f"Completed stage {stage} for work {work_id}, new stage: {WORKS_IDS[work_id]['stage']}"
    )
    return {"ok": True, "new_stage": WORKS_IDS[work_id]["stage"]}


async def error_stage(work_id: int):
    """Сообщение об ошибке на этапе работы"""
    WORKS_IDS[work_id]["stage"] = "ERROR"
    logger.info(f"Reported error for work {work_id}, new stage: ERROR")
    return {"ok": True, "new_stage": "ERROR"}
