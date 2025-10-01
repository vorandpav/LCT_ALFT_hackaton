import base64
from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont

MAIN_SERVICE_URL = "http://localhost:9002/"
USER_ID = 501
WORK_ID = 201


def draw_boxes_on_image(photo_base64, boxes):
    img = Image.open(BytesIO(base64.b64decode(photo_base64)))
    draw = ImageDraw.Draw(img)
    img_width, img_height = img.size
    font = ImageFont.truetype("arial.ttf", size=75)
    for box in boxes:
        x_center, y_center, width, height = box["bbox"]
        box_width = width * img_width
        box_height = height * img_height
        x0 = (x_center * img_width) - (box_width / 2)
        y0 = (y_center * img_height) - (box_height / 2)
        x1 = x0 + box_width
        y1 = y0 + box_height

        draw.rectangle([x0, y0, x1, y1], outline="red", width=3)
        if "predicted_name" in box:
            label = f"{box['predicted_name']} ({box['confidence']:.2f})"
        else:
            label = f"Tool ID {box['tool_id']}"
        bbox = draw.textbbox((x0, y0), label, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        draw.rectangle([x0, y0 - text_h, x0 + text_w, y0], fill="red")
        draw.text((x0, y0 - text_h), label, fill="white", font=font)

    img.show()


try:
    response = requests.get(f"{MAIN_SERVICE_URL}users/authorize/{USER_ID}/work/{WORK_ID}")
    response.raise_for_status()
    auth_data = response.json()

    stage = auth_data["stage"]

    print("Authorization Response:", auth_data, end='\n\n')
except requests.RequestException as e:
    print(f"Error during authorization: {e}\n"
          f"{e.response.json()}")
    exit(1)
except Exception as e:
    print(f"Unexpected error during authorization: {e}")
    exit(1)

try:
    response = requests.post(f"{MAIN_SERVICE_URL}works/{WORK_ID}/{stage}/complete")
    response.raise_for_status()
    complete_data = response.json()

    stage = complete_data["new_stage"]

    print("Complete Stage Response:", complete_data, end='\n\n')
except requests.RequestException as e:
    print(f"Error completing stage: {e}\n"
          f"{e.response.json()}")
    exit(1)
except Exception as e:
    print(f"Unexpected error completing stage: {e}")
    exit(1)

try:
    response = requests.get(f"{MAIN_SERVICE_URL}works/{WORK_ID}/{stage}")
    response.raise_for_status()
    work_data = response.json()

    print("Work Data Response:", work_data, end='\n\n')
except requests.RequestException as e:
    print(f"Error retrieving work data: {e}\n"
          f"{e.response.json()}")
    exit(1)
except Exception as e:
    print(f"Unexpected error retrieving work data: {e}")
    exit(1)

try:
    response = requests.post(f"{MAIN_SERVICE_URL}works/{WORK_ID}/{stage}/scan")
    response.raise_for_status()
    scan_data = response.json()

    photo_id = scan_data["photo_id"]
    photo_base64 = scan_data["photo_base64"]
    boxes = scan_data["boxes"]

    draw_boxes_on_image(photo_base64, boxes)

    print("Scan Table Response:", scan_data["photo_id"], scan_data["advice"], scan_data["boxes"], end='\n\n')
except requests.RequestException as e:
    print(f"Error during scanning: {e}\n"
          f"{e.response.json()}")
    exit(1)
except Exception as e:
    print(f"Unexpected error during scanning: {e}")
    exit(1)

try:
    for approved_box in [{'photo_id': photo_id,
                          'bbox': [0.276878, 0.462867, 0.078368, 0.279793],
                          'tool_id': 107},
                         {'photo_id': photo_id,
                          'bbox': [0.380505, 0.395509, 0.128886, 0.61658],
                          'tool_id': 102},
                         {'photo_id': photo_id,
                          'bbox': [0.485751, 0.426598, 0.090674, 0.531952],
                          'tool_id': 109},
                         {'photo_id': photo_id,
                          'bbox': [0.567034, 0.41019, 0.104275, 0.478411],
                          'tool_id': 105},
                         {'photo_id': photo_id,
                          'bbox': [0.669365, 0.413644, 0.132772, 0.400691],
                          'tool_id': 110}
                         ]:
        response = requests.post(f"{MAIN_SERVICE_URL}works/{WORK_ID}/{stage}/approve", json=approved_box)
        response.raise_for_status()
        approve_data = response.json()

        print("Approve Box Response:", approve_data, end='\n\n')
except requests.RequestException as e:
    print(f"Error approving box: {e}\n"
          f"{e.response.json()}")
    exit(1)
except Exception as e:
    print(f"Unexpected error approving box: {e}")
    exit(1)

try:
    response = requests.post(f"{MAIN_SERVICE_URL}works/{WORK_ID}/{stage}/complete")
    response.raise_for_status()
    complete_data = response.json()

    print("Complete Stage Response:", complete_data, end='\n\n')
except requests.RequestException as e:
    print(f"Error completing stage: {e}\n"
          f"{e.response.json()}")
    exit(1)
except Exception as e:
    print(f"Unexpected error completing stage: {e}")
    exit(1)

try:
    response = requests.get(f"{MAIN_SERVICE_URL}users/authorize/{USER_ID}/work/{WORK_ID}")
    response.raise_for_status()
    auth_data = response.json()

    stage = auth_data["stage"]

    print("Authorization Response:", auth_data, end='\n\n')
except requests.RequestException as e:
    print(f"Error during authorization: {e}\n"
          f"{e.response.json()}")
    exit(1)
except Exception as e:
    print(f"Unexpected error during authorization: {e}")
    exit(1)

try:
    response = requests.get(f"{MAIN_SERVICE_URL}works/{WORK_ID}/{stage}")
    response.raise_for_status()
    work_data = response.json()

    photo_data = work_data["photo_data"]
    boxes_data = work_data["approved_boxes"]

    for photo in photo_data:
        draw_boxes_on_image(photo["photo_base64"],
                            [box for box in boxes_data if box["photo_id"] == photo["photo_id"]])

    print("Work Data Response:", work_data["tid_to_tname"], boxes_data, end='\n\n')
except requests.RequestException as e:
    print(f"Error retrieving work data: {e}\n"
          f"{e.response.json()}")
    exit(1)
except Exception as e:
    print(f"Unexpected error retrieving work data: {e}")
    exit(1)

try:
    response = requests.post(f"{MAIN_SERVICE_URL}works/{WORK_ID}/{stage}/scan")
    response.raise_for_status()
    scan_data = response.json()

    photo_id = scan_data["photo_id"]
    photo_base64 = scan_data["photo_base64"]
    boxes = scan_data["boxes"]

    draw_boxes_on_image(photo_base64, boxes)

    print("Scan Table Response:", scan_data["photo_id"], scan_data["advice"], scan_data["boxes"], end='\n\n')
except requests.RequestException as e:
    print(f"Error during scanning: {e}\n"
          f"{e.response.json()}")
    exit(1)
except Exception as e:
    print(f"Unexpected error during scanning: {e}")
    exit(1)
