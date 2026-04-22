from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class LoginForm(BaseModel):
    email: EmailStr
    password: str = Field(min_length=3)


class FilterCreate(BaseModel):
    name: str
    city: str = ""
    neighborhoods: str = ""
    property_type: str = ""
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    keywords: str = ""
    owner_only: bool = True
    is_active: bool = True


class FilterOut(FilterCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ListingCreate(BaseModel):
    source: str = "manual"
    external_id: Optional[str] = None
    title: str
    description: str = ""
    price: Optional[float] = None
    neighborhood: str = ""
    city: str = ""
    property_type: str = ""
    contact_name: str = ""
    contact_phone: str = ""
    contact_role_hint: str = ""
    url: str = ""


class ListingOut(ListingCreate):
    id: int
    classification: str
    score: int
    reasons: str
    matched_filter_ids: str
    notified: bool
    created_at: datetime

    class Config:
        from_attributes = True
