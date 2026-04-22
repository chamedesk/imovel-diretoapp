from app.models import FilterProfile, Listing


def listing_matches_filter(listing: Listing, filter_profile: FilterProfile) -> bool:
    if not filter_profile.is_active:
        return False

    if filter_profile.city and listing.city.lower() != filter_profile.city.lower():
        return False

    if filter_profile.property_type and listing.property_type:
        if listing.property_type.lower() != filter_profile.property_type.lower():
            return False

    if filter_profile.min_price is not None and listing.price is not None and listing.price < filter_profile.min_price:
        return False

    if filter_profile.max_price is not None and listing.price is not None and listing.price > filter_profile.max_price:
        return False

    if filter_profile.owner_only and listing.classification == "broker_likely":
        return False

    if filter_profile.neighborhoods:
        neighborhoods = [n.strip().lower() for n in filter_profile.neighborhoods.split(",") if n.strip()]
        if neighborhoods and listing.neighborhood.lower() not in neighborhoods:
            return False

    if filter_profile.keywords:
        haystack = f"{listing.title} {listing.description}".lower()
        keywords = [k.strip().lower() for k in filter_profile.keywords.split(",") if k.strip()]
        if keywords and not any(k in haystack for k in keywords):
            return False

    return True
