from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.session import engine, Base
from app.routers import items

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Tikitoko API",
    lifespan=lifespan
)

app.include_router(items.router, prefix="/api/v1/items", tags=["items"])