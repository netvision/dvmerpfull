import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()  # Load .env before anything reads os.environ

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from database import engine, Base
import models  # noqa: F401 — import models so they register with Base metadata
from config import UPLOADS_DIR
from limiter import limiter

from routers import public, portal, users, erp


# ---------------------------------------------------------------------------
# Lifespan — create all DB tables on startup
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Lesson Plan Platform API", lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ---------------------------------------------------------------------------
# CORS — origins configured via ALLOWED_ORIGINS env var (comma-separated)
# ---------------------------------------------------------------------------
_origins_env = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173")
_allowed_origins = [o.strip() for o in _origins_env.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
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
app.include_router(erp.router, prefix="/api/portal", tags=["erp"])
app.include_router(users.router, prefix="/api/users", tags=["users"])


@app.get("/")
def root():
    return {"message": "Lesson Plan Platform API is running"}
