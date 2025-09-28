import os

PHOTO_BASE_DIR = os.getenv("PHOTO_BASE_DIR", "photos")

TEST_RESPONSES = {
    "201": ["photo_201_1.JPG", "photo_201_2.JPG", "photo_201_3.JPG"],
    "202": ["photo_202_1.JPG", "photo_202_2.JPG", "photo_202_3.JPG"],
}
