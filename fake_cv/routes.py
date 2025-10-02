import asyncio
import logging
import os
from PIL import Image
import io
from io import BytesIO

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from .storage import find_matching_file, load_result
from .config import PHOTO_DIR

router = APIRouter()
log = logging.getLogger(__name__)


@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "Fake CV Service is running"}


@router.post("/infer")
async def infer(file: UploadFile = File(...)):
    """Принимает фото и возвращает заранее подготовленный результат"""
    await asyncio.sleep(2)

    content = await file.read()
    match = find_matching_file(content)

    if not match:
        log.warning("No match for uploaded file")
        raise HTTPException(status_code=404, detail="No match for uploaded file")

    log.info(f"Matched file: {match}")
    result = load_result(match)
    return JSONResponse(content=result)


# У нас ускорит инференс ~ в 17 раз, т.к. мы сжимаем с 5 к до 1024 на 728
def resize_image(image_bytes: bytes, target_size: tuple[int, int]) -> bytes:
    """
    Изменяет размер входного изображения до target_size (ширина, высота).

    :param image_bytes: Изображение в виде байтовой строки.
    :param target_size: Кортеж (ширина, высота) для нового размера.
    :return: Измененное изображение в виде байтовой строки.
    """
    with Image.open(io.BytesIO(image_bytes)) as img:
        original_format = img.format

        # Изменяем размер. Image.Resampling.LANCZOS - это высококачественный фильтр
        # для уменьшения изображения.
        resized_img = img.resize(target_size, Image.Resampling.LANCZOS)

        # Создаем буфер в памяти для сохранения измененного изображения
        output_buffer = io.BytesIO()

        # Сохраняем изображение в буфер в его оригинальном формате
        # Если у формата нет 'JPEG', можно использовать 'PNG' как запасной вариант
        resized_img.save(output_buffer, format=original_format or 'JPEG')

        # Возвращаем байты из буфера
        return output_buffer.getvalue()


@router.post("/yolo_infer")
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

    # 1. Инициализация модели YOLO-OBB
    # model = YOLO('yolov11m-obb.pt') # или путь к вашей модели

    # 2. Выполнение предсказания.
    # results = model(resized_image_bytes)

    # 3. Обработка результатов и формирование списка словарей для JSON
    # detections_list = []
    # for r in results:
    #     for obb in r.obb: # r.obb содержит ориентированные рамки
    #         class_id = int(obb.cls)
    #         confidence = float(obb.conf) # Уверенность модели
    #         # obb.xywhr - (центр_x, центр_y, ширина, высота, угол_в_радианах)
    #         x, y, w, h, angle = obb.xywhr[0].tolist()

    #         detection_data = {
    #             "class_id": class_id,
    #             "confidence": confidence,
    #             "obb": {
    #                 "x_center": x,
    #                 "y_center": y,
    #                 "width": w,
    #                 "height": h,
    #                 "angle_rad": angle
    #             }
    #         }
    #         detections_list.append(detection_data)

    # 2. Заглушка: теперь возвращаем структуру для JSON-ответа.
    #    Вместо пустой строки создаем пустой список для обнаруженных объектов.
    detections_list = []

    # 3. Формируем финальный Python-словарь для ответа.
    #    FastAPI автоматически преобразует его в JSON.
    response_content = {
        "filename": file.filename,
        "resized_shape": {"width": target_resolution[0], "height": target_resolution[1]},
        "detections": detections_list
    }

    # 4. Возвращаем JSONResponse с нашим словарем.
    return JSONResponse(content=response_content)