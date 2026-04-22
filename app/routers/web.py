from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import FilterProfile, Listing, User
from app.services.auth import verify_password

router = APIRouter()


def current_user(request: Request, db: Session) -> User | None:
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return db.query(User).filter(User.id == user_id).first()


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return request.app.state.templates.TemplateResponse("login.html", {"request": request, "error": None})


@router.post("/login")
def login_submit(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return request.app.state.templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Credenciais inválidas."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    request.session["user_id"] = user.id
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    filters = db.query(FilterProfile).order_by(FilterProfile.created_at.desc()).all()
    listings = db.query(Listing).order_by(Listing.created_at.desc()).limit(20).all()
    stats = {
        "total_filters": db.query(FilterProfile).count(),
        "total_listings": db.query(Listing).count(),
        "owner_likely": db.query(Listing).filter(Listing.classification == "owner_likely").count(),
        "broker_likely": db.query(Listing).filter(Listing.classification == "broker_likely").count(),
    }
    return request.app.state.templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user, "filters": filters, "listings": listings, "stats": stats},
    )


@router.get("/filters/new", response_class=HTMLResponse)
def new_filter_form(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    return request.app.state.templates.TemplateResponse("new_filter.html", {"request": request, "user": user})


@router.get("/listings/new", response_class=HTMLResponse)
def new_listing_form(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    return request.app.state.templates.TemplateResponse("new_listing.html", {"request": request, "user": user})
