PHOTO_DIR = "../fake_photo_service/photos"

FAKE_CAMERA_URL = "http://localhost:9000"

FAKE_CV_URL = "http://localhost:9001"

MIDDLEWARE_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

WORK_STAGES = ["PUBLISHED", "GIVING", "IN_WORK", "GETTING", "COMPLETED", "ERROR"]

USERS_IDS = {
    501: {"user_name": "Иван Петров", "powers": "technician"},
    502: {"user_name": "Анна Смирнова", "powers": "technician"},
    503: {"user_name": "Сергей Иванов", "powers": "admin"},
}

TOOLS_IDS = {
    101: "Ключ рожковый накидной 3/4",
    102: "Отвертка '-'",
    103: "Отвертка '+'",
    104: "Отвертка на смещенный крест",
    105: "Пассатижи контровочные",
    106: "Пассатижи",
    107: "Разводной ключ",
    108: "Бокорезы",
    109: "Шэрница",
    110: "Коловорот",
    111: "Открывашка для банок с маслом",
    112: "Ключ рожковый накидной 3/4",
    113: "Отвертка '-'",
    114: "Отвертка '+'",
    115: "Отвертка на смещенный крест",
    116: "Пассатижи контровочные",
    117: "Пассатижи",
    118: "Разводной ключ",
    119: "Бокорезы",
    120: "Шэрница",
    121: "Коловорот",
    122: "Открывашка для банок с маслом",
}

TOOLS_CLASSES = {
    "Отвертка": ["Отвертка '-'", "Отвертка '+'", "Отвертка на смещенный крест"],
    "Пассатижи": ["Пассатижи контровочные", "Пассатижи"],
}

TOOLS_SETS_TYPES = {
    "standard_set": [
        "Ключ рожковый накидной 3/4",
        "Отвертка '-'",
        "Отвертка '+'",
        "Отвертка на смещенный крест",
        "Пассатижи контровочные",
        "Пассатижи" "Разводной ключ",
        "Бокорезы",
        "Шэрница",
        "Коловорот",
        "Открывашка для банок с маслом",
    ]
}

TOOLS_SETS_IDS = {
    301: {
        "set_type": "standard_set",
        "tools": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
    },
    302: {
        "set_type": "standard_set",
        "tools": [112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122],
    },
}

WORKS_IDS = {
    201: {
        "request_time_start": None,
        "request_time_end": None,
        "user_id": 501,
        "set_id": 301,
        "photo_ids_GIVING": [],
        "approved_boxes_GIVING": [],
        "photo_ids_GETTING": [],
        "approved_boxes_GETTING": [],
        "stage": "PUBLISHED",
    },
    202: {
        "request_time_start": None,
        "request_time_end": None,
        "user_id": 502,
        "set_id": 302,
        "photo_ids_GIVING": [],
        "approved_boxes_GIVING": [],
        "photo_ids_GETTING": [],
        "approved_boxes_GETTING": [],
        "stage": "PUBLISHED",
    },
}
