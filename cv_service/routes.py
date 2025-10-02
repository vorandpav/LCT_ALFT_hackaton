import logging
from PIL import Image
import math
import io
from ultralytics import YOLO

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from .config import TOOLS_MAP

router = APIRouter()
log = logging.getLogger(__name__)


@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "Fake CV Service is running"}


# @router.post("/infer")
# async def infer(file: UploadFile = File(...)):
#     """Принимает фото и возвращает заранее подготовленный результат"""
#     await asyncio.sleep(2)
#
#     content = await file.read()
#     match = find_matching_file(content)
#
#     if not match:
#         log.warning("No match for uploaded file")
#         raise HTTPException(status_code=404, detail="No match for uploaded file")
#
#     log.info(f"Matched file: {match}")
#     result = load_result(match)
#     return JSONResponse(content=result)


def resize_image(image_bytes: bytes, target_size: tuple[int, int]) -> bytes:
    """
    Изменяет размер входного изображения до target_size (ширина, высота).
    """
    with Image.open(io.BytesIO(image_bytes)) as img:
        original_format = img.format

        resized_img = img.resize(target_size, Image.Resampling.LANCZOS)

        output_buffer = io.BytesIO()

        resized_img.save(output_buffer, format=original_format or 'JPEG')

        return output_buffer.getvalue()


def obb_to_corners(x_center, y_center, width, height, angle_rad):
    """
    Преобразует OBB параметры в 8 координат углов
    """

    half_w = width / 2
    half_h = height / 2

    corners = [
        [-half_w, -half_h],
        [half_w, -half_h],
        [half_w, half_h],
        [-half_w, half_h]
    ]

    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    rotated_corners = []
    for x, y in corners:
        x_rot = x * cos_a - y * sin_a
        y_rot = x * sin_a + y * cos_a
        rotated_corners.append(x_center + x_rot)
        rotated_corners.append(y_center + y_rot)

    return rotated_corners


@router.post("/infer")
async def yolo_infer(file: UploadFile = File(...)):
    """Принимает изображение и возвращает разметку от YOLO в формате JSON."""

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image.")

    image_bytes = await file.read()

    try:
        target_resolution = (1024, 728)
        resized_image_bytes = resize_image(image_bytes, target_resolution)
        log.info(f"Image resized to {target_resolution}")
    except Exception as e:
        log.error(f"Failed to resize image: {e}")
        raise HTTPException(status_code=500, detail="Image processing failed.")

    model = YOLO('yolo_model.pt')

    pil_image = Image.open(io.BytesIO(resized_image_bytes))
    results = model(pil_image)

    detections_list = []
    for r in results:
        for obb in r.obb:
            class_id = int(obb.cls)
            confidence = float(obb.conf)
            x, y, w, h, angle = obb.xywhr[0].tolist()

            bbox_cords_pixels = obb_to_corners(x, y, w, h, angle)

            img_height, img_width = r.orig_shape[:2]
            bbox_cords_normalized = [
                coord / img_width if i % 2 == 0 else coord / img_height
                for i, coord in enumerate(bbox_cords_pixels)
            ]

            detection_data = {
                "predicted_class": TOOLS_MAP[class_id],
                "confidence": confidence,
                "bbox": bbox_cords_normalized
            }
            detections_list.append(detection_data)
    response_content = {
        "detections": detections_list
    }

    return JSONResponse(content=response_content)
