from __future__ import annotations

from dataclasses import dataclass


OWNER_SIGNALS = [
    "direto com proprietário",
    "direto com proprietario",
    "sem corretor",
    "particular",
    "sou o dono",
    "sou a dona",
    "proprietário",
    "proprietario",
    "meu imóvel",
    "meu imovel",
    "trato direto",
]

BROKER_SIGNALS = [
    "creci",
    "corretor",
    "corretora",
    "imobiliária",
    "imobiliaria",
    "consultor imobiliário",
    "consultor imobiliario",
    "broker",
    "avaliamos seu imóvel",
    "avaliamos seu imovel",
    "angariamos",
]

NEGATED_BROKER_PHRASES = [
    "sem corretor",
    "dispenso corretor",
    "não aceito corretor",
    "nao aceito corretor",
]


@dataclass
class ClassificationResult:
    label: str
    score: int
    reasons: list[str]


def classify_listing(title: str, description: str, contact_role_hint: str = "") -> ClassificationResult:
    text = f"{title} {description} {contact_role_hint}".lower().strip()
    score = 50
    reasons: list[str] = []

    for signal in OWNER_SIGNALS:
        if signal in text:
            score += 12
            reasons.append(f"Sinal de proprietário: '{signal}'")

    for signal in BROKER_SIGNALS:
        if signal in text:
            if signal in {"corretor", "corretora"} and any(neg in text for neg in NEGATED_BROKER_PHRASES):
                reasons.append("Menção a corretor em contexto de negação")
                continue
            score -= 15
            reasons.append(f"Sinal de corretor: '{signal}'")

    if contact_role_hint.lower() in {"owner", "proprietario", "proprietário"}:
        score += 15
        reasons.append("Contato marcado como proprietário")

    if contact_role_hint.lower() in {"broker", "corretor", "imobiliaria", "imobiliária"}:
        score -= 20
        reasons.append("Contato marcado como corretor/imobiliária")

    score = max(0, min(100, score))

    if score >= 70:
        label = "owner_likely"
    elif score <= 35:
        label = "broker_likely"
    else:
        label = "uncertain"

    if not reasons:
        reasons.append("Sem sinais fortes; manter revisão humana")

    return ClassificationResult(label=label, score=score, reasons=reasons)
