"""Cechy morze i centrum z opisu przez stemming

każde słowo jest stemowane tym samym stemmerem
co dokument, więc dopasowanie jest na poziomie morfemu słowa 
"""

from __future__ import annotations

import re
from Stemmer import Stemmer as PyStemmerStemmer

from repozytorium.features.text_processing import tokenizuj_slowa

STEMMER_ET = PyStemmerStemmer("estonian")

# Reprezentatywne formy słów 
_SLOWA_REF_MORZE = (
    "meri",
    "mere",
    "rand",
    "ranna",
    "rannik",
    "supelrand",
    "promenaad",
    "sadam",
    "laht",
    "vaade",
    "kalju",
)

_SLOWA_REF_CENTRUM = (
    "kesklinn",
    "vanalinn",
    "südalinn",
    "keskus",
    "peatänav",
    "kesklinnas",
)

KORZENIE_REF_MORZE = frozenset(STEMMER_ET.stemWords(list(_SLOWA_REF_MORZE)))
KORZENIE_REF_CENTRUM = frozenset(STEMMER_ET.stemWords(list(_SLOWA_REF_CENTRUM)))


def _zbior_korzeni_z_tekstu(tekst: str | None) -> frozenset[str]:
    if not tekst or not isinstance(tekst, str):
        return frozenset()
    tokeny = tokenizuj_slowa(tekst)
    if not tokeny:
        return frozenset()
    return frozenset(STEMMER_ET.stemWords(tokeny))


def cechy_lokalizacji_z_korzeni(opis: str | None) -> dict[str, float]:
    """Zmienne binarne"""

    korzenie_dok = _zbior_korzeni_z_tekstu(opis)
    return {
        "nlp_bliskosc_morza": float(bool(korzenie_dok & KORZENIE_REF_MORZE)),
        "nlp_centrum_miasta": float(bool(korzenie_dok & KORZENIE_REF_CENTRUM)),
    }


def wyciagnij_cechy_z_lematow_string(lematy_spacja: str | None) -> dict[str, float]:
    """Te same cechy ale liczone na już zlematyzowanym łańcuchu """

    if not lematy_spacja or not isinstance(lematy_spacja, str):
        return {"nlp_bliskosc_morza": 0.0, "nlp_centrum_miasta": 0.0}
    tokeny = [t for t in re.split(r"\s+", lematy_spacja.strip()) if t]
    if not tokeny:
        return {"nlp_bliskosc_morza": 0.0, "nlp_centrum_miasta": 0.0}
    # Lematy traktujemy jak tokeny — porównanie przez stem dla spójności z synonimami.
    korzenie_dok = frozenset(STEMMER_ET.stemWords(tokeny))
    return {
        "nlp_bliskosc_morza": float(bool(korzenie_dok & KORZENIE_REF_MORZE)),
        "nlp_centrum_miasta": float(bool(korzenie_dok & KORZENIE_REF_CENTRUM)),
    }


def nazwy_cech_lokalizacji_nlp() -> tuple[str, ...]:
    """Nazwy kolumn """

    return ("nlp_bliskosc_morza", "nlp_centrum_miasta")
