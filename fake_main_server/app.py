from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fake_main_server.routers import users, works, sets
from fake_main_server.config import MIDDLEWARE_ORIGINS


def create_app() -> FastAPI:
    app = FastAPI(title="Main Server", version="0.1")

    app.include_router(users.router, prefix="/users", tags=["users"])
    app.include_router(works.router, prefix="/works", tags=["works"])
    app.include_router(sets.router, prefix="/sets", tags=["sets"])

    app.add_middleware(
        CORSMiddleware,
        allow_origins=MIDDLEWARE_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    async def health_check():
        return {"status": "ok", "message": "Main Server is running"}

    return app
