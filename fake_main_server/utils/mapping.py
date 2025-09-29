from fake_main_server.config import TOOLS_CLASSES, TOOLS_IDS


def map_tool_class_to_names(predicted_class: str, tools_ids: set[int]) -> list[str]:
    """Сопоставляет класс модели с конкретными названиями инструментов из множества tools_ids."""
    if predicted_class in TOOLS_CLASSES:
        possible_names = TOOLS_CLASSES[predicted_class]
        matched_names = [TOOLS_IDS[tid] for tid in tools_ids if TOOLS_IDS[tid] in possible_names]
        return matched_names
    elif predicted_class in TOOLS_IDS.values():
        if predicted_class in [TOOLS_IDS[tid] for tid in tools_ids]:
            return [predicted_class]
        else:
            return []
    raise ValueError(f"Unknown predicted class: {predicted_class}")
