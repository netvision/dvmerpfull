import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import engine, Base
import models  # noqa: F401 — import models so they register with Base metadata
from config import UPLOADS_DIR

from routers import public, portal, users


# ---------------------------------------------------------------------------
# Lifespan — create all DB tables on startup
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Lesson Plan Platform API", lifespan=lifespan)

# ---------------------------------------------------------------------------
# CORS — allow local Vite dev server
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Static files — uploads directory
# ---------------------------------------------------------------------------
os.makedirs(UPLOADS_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(public.router, prefix="/api/public", tags=["public"])
app.include_router(portal.router, prefix="/api/portal", tags=["portal"])
app.include_router(users.router, prefix="/api/users", tags=["users"])


@app.get("/")
def root():
    return {"message": "Lesson Plan Platform API is running"}
