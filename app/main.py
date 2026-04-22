from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.templating import Jinja2Templates

from app.core.config import settings
from app.core.database import Base, SessionLocal, engine
from app.routers.api import router as api_router
from app.routers.web import router as web_router
from app.services.auth import ensure_admin_user

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title=settings.app_name)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.state.templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        ensure_admin_user(db)
    finally:
        db.close()


app.include_router(web_router)
app.include_router(api_router)


@app.get("/health")
def health():
    return {"status": "ok", "app": settings.app_name, "env": settings.app_env}
