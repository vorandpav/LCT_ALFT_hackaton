from fake_main_server.config import TOOLS_CLASSES, TOOLS_IDS, TOOLS_SETS_IDS


def map_prediction_to_tools(predicted_class: str, set_id: int):
    """Сопоставляет класс модели с конкретными инструментами из набора"""
    tools_in_set = TOOLS_SETS_IDS[set_id]["tools"]

    # если класс конкретный → сразу возвращаем
    if predicted_class in TOOLS_IDS.values():
        return [tid for tid, name in TOOLS_IDS.items() if name == predicted_class and tid in tools_in_set]

    # если класс — общий (например "Отвёртка")
    if predicted_class in TOOLS_CLASSES:
        return [
            tid for tid, name in TOOLS_IDS.items()
            if name in TOOLS_CLASSES[predicted_class] and tid in tools_in_set
        ]

    # если класс не известен
    raise ValueError(f"Unknown predicted class: {predicted_class}")
