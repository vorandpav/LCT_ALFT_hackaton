from fastapi import FastAPI
from routes import users, works, sets


def create_app() -> FastAPI:
    app = FastAPI(title="Main Server", version="0.1")

    app.include_router(users.router, prefix="/users", tags=["users"])
    app.include_router(works.router, prefix="/works", tags=["works"])
    app.include_router(sets.router, prefix="/sets", tags=["sets"])

    @app.get("/health")
    async def health_check():
        return {"status": "ok", "message": "Main Server is running"}

    return app
