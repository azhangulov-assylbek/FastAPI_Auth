import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from app.api.routers import users, auth
from app.db.database import Base, engine
from app.db import models  # noqa: F401 — регистрирует модели в Base.metadata для create_all


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}






if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)