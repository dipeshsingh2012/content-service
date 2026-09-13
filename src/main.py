from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.api.routes import router as api_router
from src.config import settings
from src.db.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.DATABASE_URL:
        try:
            from sqlalchemy import text
            from src.db.database import Base, get_sessionmaker
            from src.db.seed import seed_cms_data
            async with engine.begin() as conn:
                await conn.execute(text("ALTER TABLE cms_site_shell ADD COLUMN IF NOT EXISTS theme JSONB DEFAULT '{}'::jsonb;"))
                await conn.run_sync(Base.metadata.create_all)
            session_factory = get_sessionmaker()
            async with session_factory() as session:
                await seed_cms_data(session)
        except Exception as e:
            print(f"Startup DB init warning: {e}")
    yield
    if settings.DATABASE_URL:
        try:
            await engine.dispose()
        except Exception:
            pass




app = FastAPI(
    title="Hiljhil Cafe - Content & Merchandising CMS API",
    summary="Headless Content Engine for Circular Category Lanes, Product Sliders, Navigation and Editorial Pages.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count"],
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {
        "message": "Content & Merchandising CMS Service is running",
        "service": "content-service",
        "version": "0.1.0",
        "docs_url": "/docs",
        "health_url": "/api/v1/health",
    }


if __name__ == "__main__":
    uvicorn.run("src.main:app", host=settings.HOST, port=settings.PORT, reload=True)
