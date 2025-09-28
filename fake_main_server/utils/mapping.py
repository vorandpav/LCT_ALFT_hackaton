from fake_main_server.config import TOOLS_CLASSES, TOOLS_IDS, TOOLS_SETS_IDS


def map_tool_class_to_names(predicted_class: str, set_id: int) -> list[str]:
    """Сопоставляет класс модели с конкретными названиями инструментов из набора."""
    tools_in_set = TOOLS_SETS_IDS[set_id]["tools"]

    # если класс конкретный → сразу возвращаем
    if predicted_class in TOOLS_IDS.values():
        return [predicted_class]

    # если класс — общий (например "Отвёртка")
    if predicted_class in TOOLS_CLASSES:
        return [
            name for tid, name in TOOLS_IDS.items()
            if name in TOOLS_CLASSES[predicted_class] and tid in tools_in_set
        ]

    # если класс не известен
    raise ValueError(f"Unknown predicted class: {predicted_class}")
