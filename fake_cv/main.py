import uvicorn
from .app import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("fake_cv.main:app", host="0.0.0.0", port=9100, reload=True)
