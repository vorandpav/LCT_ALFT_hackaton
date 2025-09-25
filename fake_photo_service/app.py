from fastapi import FastAPI
from .routes import router

def create_app() -> FastAPI:
    app = FastAPI(title="Fake Camera Service")
    app.include_router(router)
    return app
