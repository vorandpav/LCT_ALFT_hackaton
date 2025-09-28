def generate_id(work_id: int, stage: str) -> str:
    """Генерация id фото"""
    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{work_id}_{stage}_{ts}.jpg"
