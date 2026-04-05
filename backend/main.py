from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
import models  # noqa: F401 — import models so they register with Base metadata

from routers import public, portal, users

app = FastAPI(title="Lesson Plan Platform API")

# ---------------------------------------------------------------------------
# CORS — allow all origins for local development
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(public.router, prefix="/api/public", tags=["public"])
app.include_router(portal.router, prefix="/api/portal", tags=["portal"])
app.include_router(users.router, prefix="/api/users", tags=["users"])


# ---------------------------------------------------------------------------
# Startup event — create all DB tables
# ---------------------------------------------------------------------------
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Lesson Plan Platform API is running"}
