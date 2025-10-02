import os

import requests
from PIL import Image, ImageDraw, ImageFont

CV_SERVICE_URL = "http://localhost:9001/infer"

PHOTO_PATH = "../fake_photo_service/photos/201_1.JPG"

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
    font = ImageFont.truetype("arial.ttf", size=20)

    for det in cv_data.get("detections", []):
        coords = det["bbox"]
        points = [
            (coords[i] * img_width, coords[i + 1] * img_height)
            for i in range(0, len(coords), 2)
        ]

        draw.polygon(points, outline="red", width=3)

        x0, y0 = points[0]
        label = f"{det['predicted_class']} ({det['confidence']:.2f})"

        bbox = draw.textbbox((x0, y0), label, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        draw.rectangle([x0, y0 - text_h, x0 + text_w, y0], fill="red")
        draw.text((x0, y0 - text_h), label, fill="white", font=font)

    img.show()

except requests.RequestException as e:
    print(f"Error communicating with CV service: {e}")
    if e.response:
        print(f"Response: {e.response.json()}")
