import io
from datetime import datetime
import os
from PIL import Image
from fake_main_server.config import PHOTO_DIR


def generate_id(work_id: str, stage: str) -> str:
    """
    Генерация id фото на основе work_id, стадии и времени.
    """
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{work_id}_{stage}_{ts}.jpg"


def save(photo_bytes: bytes, photo_name: str):
    """
    Проверяет и сохраняет фото в файловую систему.
    """
    path = os.path.join(PHOTO_DIR, photo_name)
    if os.path.exists(path):
        raise ValueError(f"File with this name already exists: {photo_name}")
    try:
        image_stream = io.BytesIO(photo_bytes)
        with Image.open(image_stream) as img:
            img.verify()
    except (IOError, SyntaxError, Image.DecompressionBombError) as e:
        raise ValueError(f"Provided data is not a valid image: {e}")
    with open(path, "wb") as f:
        f.write(photo_bytes)


def load(photo_name: str) -> bytes:
    """
    Загружает фото из файловой системы как байты.
    """
    path = os.path.join(PHOTO_DIR, photo_name)
    if not os.path.exists(path):
        raise ValueError(f"File not found: {photo_name}")
    try:
        with Image.open(path) as img:
            img.verify()
    except (IOError, SyntaxError) as e:
        raise ValueError(f"File on disk is corrupted: {e}")
    with open(path, "rb") as f:
        return f.read()
