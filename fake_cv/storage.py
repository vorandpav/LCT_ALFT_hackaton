import os
import json
import hashlib
from fastapi import HTTPException, UploadFile
from .config import PHOTO_DIR, TEST_RESPONSES


def file_md5(file_path: str) -> str:
    """Вычисляет md5-хеш файла"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def find_matching_file(upload: UploadFile) -> str | None:
    """
    Сравнивает загруженное фото с тестовыми.
    Возвращает имя файла (например "photo_123_1.jpg") или None.
    """
    content = upload.file.read()
    upload.file.seek(0)  # сбросить указатель, чтобы можно было читать ещё раз

    upload_hash = hashlib.md5(content).hexdigest()

    for fname in TEST_RESPONSES:
        test_path = os.path.join(PHOTO_DIR, fname)
        if os.path.exists(test_path):
            if file_md5(test_path) == upload_hash:
                return fname
    return None


def load_result(fname: str):
    """Загружает результат из TEST_RESPONSES по имени файла"""
    if fname not in TEST_RESPONSES:
        raise HTTPException(status_code=404, detail="Test response not found")
    return TEST_RESPONSES[fname]
