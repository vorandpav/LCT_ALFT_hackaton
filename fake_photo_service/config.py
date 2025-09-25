import os

PHOTO_BASE_DIR = os.getenv("PHOTO_BASE_DIR", "./photos")

TEST_RESPONSES = {
    "123": ["photo_123_1.jpg", "photo_123_2.jpg", "photo_123_3.jpg"],
    "456": ["photo_456_1.jpg", "photo_456_2.jpg", "photo_456_3.jpg"],
}
