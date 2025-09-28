from datetime import datetime
import os
from PIL import Image
from fake_main_server.config import PHOTO_DIR


def generate_id(work_id: int, stage: str) -> str:
    """Генерация id фото"""
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{work_id}_{stage}_{ts}.jpg"


def save(photo: bytes, photo_name: str):
    """Сохраняет фото в файловую систему"""
    if os.path.exists(os.path.join(PHOTO_DIR, photo_name)):
        raise ValueError("File with this ID already exists")

    path = os.path.join(PHOTO_DIR, photo_name)
    with open(path, "wb") as f:
        f.write(photo)

    try:
        img = Image.open(path)
        img.verify()
    except (IOError, SyntaxError) as e:
        os.remove(path)
        raise ValueError(f"Saved file is not a valid image: {e}")


def load(photo_name: str):
    """Загружает фото из файловой системы"""
    path = os.path.join(PHOTO_DIR, photo_name)
    if not os.path.exists(path):
        raise ValueError("File not found")

    # Проверка файла перед чтением
    try:
        img = Image.open(path)
        img.verify()
    except (IOError, SyntaxError) as e:
        raise ValueError(f"Invalid image file: {e}")

    with open(path, "rb") as f:
        return f.read()
