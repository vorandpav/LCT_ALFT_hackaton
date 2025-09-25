import uvicorn
from .app import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("fake_camera.main:app", host="0.0.0.0", port=9000, reload=True)
