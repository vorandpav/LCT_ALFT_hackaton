import os

PHOTO_DIR = os.getenv("PHOTO_DIR", "photos")

TEST_RESPONSES = {
    "photo_201_1.JPG": {
        "advice": "ok",
        "detections": [
            {
                "bbox": [0.276878, 0.462867, 0.078368, 0.279793],
                "predicted_class": "Ключ рожковый накидной 3/4",
                "confidence": 0.95
            },
            {
                "bbox": [0.380505, 0.395509, 0.128886, 0.616580],
                "predicted_class": "Отвертка",
                "confidence": 0.92
            },
            {
                "bbox": [0.485751, 0.426598, 0.090674, 0.531952],
                "predicted_class": "Пассатижи",
                "confidence": 0.88
            },
            {
                "bbox": [0.567034, 0.410190, 0.104275, 0.478411],
                "predicted_class": "Пассатижи",
                "confidence": 0.85
            },
            {
                "bbox": [0.669365, 0.413644, 0.132772, 0.400691],
                "predicted_class": "Шэрница",
                "confidence": 0.83
            },
            {
                "bbox": [0.792098, 0.422712, 0.113990, 0.541451],
                "predicted_class": "Отвертка",
                "confidence": 0.80
            },
            {
                "bbox": [0.895078, 0.417530, 0.142487, 0.517271],
                "predicted_class": "Разводной ключ",
                "confidence": 0.78
            },
            {
                "bbox": [0.949806, 0.394214, 0.100388, 0.334197],
                "predicted_class": "Коловорот",
                "confidence": 0.75
            },
            {
                "bbox": [0.714378, 0.859672, 0.571244, 0.280656],
                "predicted_class": "Открывашка для банок с маслом",
                "confidence": 0.70
            }
        ]
    },

    "photo_201_2.JPG": {
        "advice": "ok",
        "detections": [
            {
                "bbox": [0.297604, 0.268135, 0.548575, 0.417098],
                "predicted_class": "Разводной ключ",
                "confidence": 0.90
            },
            {
                "bbox": [0.258096, 0.376511, 0.218264, 0.405872],
                "predicted_class": "Отвертка",
                "confidence": 0.85
            },
            {
                "bbox": [0.367552, 0.392919, 0.197539, 0.343696],
                "predicted_class": "Шэрница",
                "confidence": 0.87
            },
            {
                "bbox": [0.377915, 0.531952, 0.139249, 0.490501],
                "predicted_class": "Пассатижи",
                "confidence": 0.83
            },
            {
                "bbox": [0.502267, 0.373921, 0.169041, 0.407599],
                "predicted_class": "Пассатижи",
                "confidence": 0.82
            },
            {
                "bbox": [0.560233, 0.503022, 0.139896, 0.417098],
                "predicted_class": "Коловорот",
                "confidence": 0.80
            },
            {
                "bbox": [0.727332, 0.632124, 0.270725, 0.283247],
                "predicted_class": "Открывашка для банок с маслом",
                "confidence": 0.78
            },
            {
                "bbox": [0.748381, 0.409326, 0.235104, 0.271157],
                "predicted_class": "Отвертка",
                "confidence": 0.76
            },
            {
                "bbox": [0.787565, 0.652418, 0.172280, 0.163212],
                "predicted_class": "Ключ рожковый накидной 3/4",
                "confidence": 0.74
            },
            {
                "bbox": [0.737694, 0.219775, 0.321244, 0.360104],
                "predicted_class": "Бокорезы",
                "confidence": 0.72
            },
            {
                "bbox": [0.732837, 0.277202, 0.277850, 0.245250],
                "predicted_class": "Отвертка",
                "confidence": 0.70
            }
        ]
    },
    "photo_201_3.JPG": {
        "advice": "ok",
        "detections": [
            {
                "bbox": [0.368199, 0.557858, 0.612047, 0.526770],
                "predicted_class": "Разводной ключ",
                "confidence": 0.90
            },
            {
                "bbox": [0.375648, 0.259067, 0.242228, 0.390328],
                "predicted_class": "Открывашка для банок с маслом",
                "confidence": 0.88
            },
            {
                "bbox": [0.471179, 0.360967, 0.233808, 0.326425],
                "predicted_class": "Шэрница",
                "confidence": 0.86
            },
            {
                "bbox": [0.595207, 0.351468, 0.259067, 0.317789],
                "predicted_class": "Пассатижи",
                "confidence": 0.84
            },
            {
                "bbox": [0.715997, 0.312608, 0.143135, 0.416235],
                "predicted_class": "Отвертка",
                "confidence": 0.82
            },
            {
                "bbox": [0.751619, 0.474093, 0.091321, 0.331606],
                "predicted_class": "Отвертка",
                "confidence": 0.80
            },
            {
                "bbox": [0.817034, 0.475820, 0.060233, 0.417962],
                "predicted_class": "Коловорот",
                "confidence": 0.78
            },
            {
                "bbox": [0.678433, 0.675302, 0.166451, 0.063903],
                "predicted_class": "Ключ рожковый накидной 3/4",
                "confidence": 0.76
            },
            {
                "bbox": [0.881801, 0.570812, 0.219560, 0.450777],
                "predicted_class": "Бокорезы",
                "confidence": 0.74
            },
            {
                "bbox": [0.507124, 0.620466, 0.357513, 0.185665],
                "predicted_class": "Пассатижи",
                "confidence": 0.72
            },
            {
                "bbox": [0.492228, 0.564767, 0.329016, 0.129534],
                "predicted_class": "Отвертка",
                "confidence": 0.70
            }
        ]
    }
}
