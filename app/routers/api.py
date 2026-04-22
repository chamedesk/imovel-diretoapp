from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models import FilterProfile, Listing
from app.schemas import FilterCreate, FilterOut, ListingCreate, ListingOut
from app.services.classifier import classify_listing
from app.services.filtering import listing_matches_filter
from app.services.notifier import send_telegram_alert

router = APIRouter(prefix="/api", tags=["api"])


@router.post("/filters", response_model=FilterOut)
def create_filter(payload: FilterCreate, db: Session = Depends(get_db)):
    filter_profile = FilterProfile(**payload.model_dump())
    db.add(filter_profile)
    db.commit()
    db.refresh(filter_profile)
    return filter_profile


@router.get("/filters", response_model=list[FilterOut])
def list_filters(db: Session = Depends(get_db)):
    return db.query(FilterProfile).order_by(FilterProfile.created_at.desc()).all()


@router.post("/listings", response_model=ListingOut)
def create_listing(payload: ListingCreate, db: Session = Depends(get_db)):
    if payload.external_id:
        existing = db.query(Listing).filter(
            Listing.source == payload.source,
            Listing.external_id == payload.external_id,
        ).first()
        if existing:
            return existing

    result = classify_listing(payload.title, payload.description, payload.contact_role_hint)
    listing = Listing(
        **payload.model_dump(),
        classification=result.label,
        score=result.score,
        reasons=" | ".join(result.reasons),
    )
    db.add(listing)
    db.flush()

    filters = db.query(FilterProfile).all()
    matched_ids: list[str] = []
    for filter_profile in filters:
        if listing_matches_filter(listing, filter_profile):
            matched_ids.append(str(filter_profile.id))

    listing.matched_filter_ids = ",".join(matched_ids)

    should_notify = listing.classification == "owner_likely" and listing.score >= settings.alert_min_score and bool(matched_ids)
    if should_notify:
        listing.notified = send_telegram_alert(listing)

    db.commit()
    db.refresh(listing)
    return listing


@router.get("/listings", response_model=list[ListingOut])
def list_listings(db: Session = Depends(get_db)):
    return db.query(Listing).order_by(Listing.created_at.desc()).all()


@router.post("/listings/{listing_id}/recheck", response_model=ListingOut)
def recheck_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado")

    result = classify_listing(listing.title, listing.description, listing.contact_role_hint)
    listing.classification = result.label
    listing.score = result.score
    listing.reasons = " | ".join(result.reasons)
    db.commit()
    db.refresh(listing)
    return listing
