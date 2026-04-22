import requests

from app.core.config import settings
from app.models import Listing


def send_telegram_alert(listing: Listing) -> bool:
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        return False

    text = (
        f"🏠 Novo anúncio classificado\n"
        f"Título: {listing.title}\n"
        f"Classificação: {listing.classification} ({listing.score})\n"
        f"Bairro: {listing.neighborhood or '-'}\n"
        f"Cidade: {listing.city or '-'}\n"
        f"Preço: {listing.price or '-'}\n"
        f"Fonte: {listing.source}\n"
        f"Link: {listing.url or '-'}"
    )

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    response = requests.post(url, json={"chat_id": settings.telegram_chat_id, "text": text}, timeout=15)
    return response.ok
