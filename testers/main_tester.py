import base64
from io import BytesIO

import requests
import os

from PIL import Image, ImageDraw, ImageFont

MAIN_SERVICE_URL = "http://localhost:9002/"
USER_ID = 501
WORK_ID = 201

try:
    response = requests.get(f"{MAIN_SERVICE_URL}users/authorize/{USER_ID}/work/{WORK_ID}")
    response.raise_for_status()
    auth_data = response.json()
    stage = auth_data["stage"]
    print("Authorization Response:", auth_data)
except requests.RequestException as e:
    print(f"Error during authorization: {e}\n"
          f"{e.response.json()}")
    exit(1)

try:
    response = requests.post(f"{MAIN_SERVICE_URL}works/{WORK_ID}/{stage}/complete")
    response.raise_for_status()
    complete_data = response.json()
    stage = complete_data["new_stage"]
    print("Complete Stage Response:", complete_data)
except requests.RequestException as e:
    print(f"Error completing stage: {e}\n"
          f"{e.response.json()}")
    exit(1)

try:
    response = requests.get(f"{MAIN_SERVICE_URL}works/{WORK_ID}/{stage}")
    response.raise_for_status()
    work_data = response.json()
    print("Work Data Response:", work_data)
except requests.RequestException as e:
    print(f"Error retrieving work data: {e}\n"
          f"{e.response.json()}")
    exit(1)

try:
    response = requests.post(f"{MAIN_SERVICE_URL}works/{WORK_ID}/{stage}/scan")
    response.raise_for_status()
    scan_data = response.json()
    photo_base64 = scan_data["photo_base64"]
    img = Image.open(BytesIO(base64.b64decode(photo_base64)))
    img.show()
    print("Scan Table Response:", scan_data["photo_name"], scan_data["advice"], scan_data["boxes"])
except:
    print(f"Error during scanning: {e}\n"
          f"{e.response.json()}")
    exit(1)
