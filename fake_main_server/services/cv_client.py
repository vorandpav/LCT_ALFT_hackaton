import httpx

FAKE_CV_URL = "http://localhost:8002"


async def infer(photo):
    files = {"file": ("photo.jpg", bytes.fromhex(photo["photo_data"]), "image/jpeg")}
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{FAKE_CV_URL}/infer", files=files)
        resp.raise_for_status()
        return resp.json()
