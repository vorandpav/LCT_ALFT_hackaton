import os

PHOTO_BASE_DIR = os.getenv("PHOTO_BASE_DIR", "./photos")

TEST_RESPONSES = {
    "201": ["photo_201_1.jpg", "photo_201_2.jpg", "photo_201_3.jpg"],
    "202": ["photo_202_1.jpg", "photo_202_2.jpg", "photo_202_3.jpg"],
}
