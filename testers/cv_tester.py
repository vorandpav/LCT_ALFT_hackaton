import os

import requests
from PIL import Image, ImageDraw, ImageFont

CV_SERVICE_URL = "http://localhost:9001/infer"

PHOTO_PATH = "../fake_photo_service/photos/photo_201_1.JPG"

try:
    with open(PHOTO_PATH, "rb") as image_file:
        files = {"file": (os.path.basename(PHOTO_PATH), image_file, "image/jpeg")}
        response = requests.post(CV_SERVICE_URL, files=files)
        response.raise_for_status()

    cv_data = response.json()
    print("CV Service Response:", cv_data)

    img = Image.open(PHOTO_PATH)
    draw = ImageDraw.Draw(img)
    img_width, img_height = img.size
    font = ImageFont.truetype("arial.ttf", size=75)

    for det in cv_data.get("detections", []):
        x_center, y_center, width, height = det["bbox"]

        box_width = width * img_width
        box_height = height * img_height
        x0 = (x_center * img_width) - (box_width / 2)
        y0 = (y_center * img_height) - (box_height / 2)
        x1 = x0 + box_width
        y1 = y0 + box_height

        draw.rectangle([x0, y0, x1, y1], outline="red", width=3)

        label = f"{det['predicted_class']} ({det['confidence']:.2f})"
        bbox = draw.textbbox((x0, y0), label, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        draw.rectangle([x0, y0 - text_h, x0 + text_w, y0], fill="red")
        draw.text((x0, y0 - text_h), label, fill="white", font=font)

    img.show()

except requests.RequestException as e:
    print(f"Error communicating with CV service: {e}" f"{e.response.json()}")
