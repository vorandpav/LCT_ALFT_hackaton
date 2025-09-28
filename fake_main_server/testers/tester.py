import requests
import os

from PIL import Image, ImageDraw, ImageFont

MAIN_SERVICE_URL = "http://localhost:9002/"
USER_ID = 501
WORK_ID = 201


def test_main_server():
    try:
        response = requests.get(f"{MAIN_SERVICE_URL}users/authorize/{USER_ID}/work/{WORK_ID}")
        response.raise_for_status()
        auth_data = response.json()
        print("Authorization Response:", auth_data)
    except requests.RequestException as e:
        print(f"Error during authorization: {e}\n"
              f"{e.response.json()}")


if __name__ == "__main__":
    test_main_server()
