import requests
from PIL import Image
from io import BytesIO

work_id = 202
url = f"http://localhost:9000/{work_id}"

try:
    response = requests.get(url)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"Error fetching photo: {e}\n"
          f"{e.response.json()}")
    exit(1)

img = Image.open(BytesIO(response.content))
img.show()
