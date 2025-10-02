import asyncio
import logging
import os
from PIL import Image
import io
from io import BytesIO

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse

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


@router.post("/yolo_infer", response_class=StreamingResponse)
async def yolo_infer(file: UploadFile = File(...)):
    """Принимает изображение и возвращает разметку от YOLO в txt файле."""

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image.")

    image_bytes = await file.read()

    # Изменение размера изображения
    try:
        target_resolution = (1024, 728)
        resized_image_bytes = resize_image(image_bytes, target_resolution)
        log.info(f"Image resized to {target_resolution}")
    except Exception as e:
        log.error(f"Failed to resize image: {e}")
        raise HTTPException(status_code=500, detail="Image processing failed.")

    # 1. Инициализация модели YOLO-OBB
    # model = YOLO('yolov8n-obb.pt')  # или путь к вашей модели

    # 2. Выполнение предсказания.
    # results = model(resized_image_bytes)  # results - это список объектов Results

    # 3. Обработка результатов и формирование txt файла
    # output_lines = []
    # for r in results:
    #     for obb in r.obb:  # r.obb содержит ориентированные рамки
    #         # Формат xywhr: (центр_x, центр_y, ширина, высота, угол_в_радианах)
    #         # Координаты обычно нормализованы (от 0 до 1)
    #         class_id = int(obb.cls)
    #         x_center, y_center, w, h, angle = obb.xywhr[0].tolist()
    #         output_lines.append(f"{class_id} {x_center} {y_center} {w} {h} {angle}")

    # output_string = "\n".join(output_lines)

    # Заглушка: возвращаем пустую строку
    output_string = ""

    # Преобразование строки в байты для отправки
    output_bytes = output_string.encode('utf-8')

    # Создание файлоподобного объекта в памяти
    string_io = io.BytesIO(output_bytes)

    # Получение оригинального имени файла без расширения
    base_filename = os.path.splitext(file.filename)[0]

    # Установка заголовков для скачивания файла
    headers = {
        'Content-Disposition': f'attachment; filename="{base_filename}.txt"'
    }

    return StreamingResponse(string_io, media_type="text/plain", headers=headers)