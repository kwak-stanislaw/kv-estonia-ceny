"""Cechy tekstowe

Moduł ``cechy_lokalizacji_nlp`` — morfemy Snowball dla estońskiego
"""

from __future__ import annotations

import re

from repozytorium.features.cechy_lokalizacji_nlp import (
    cechy_lokalizacji_z_korzeni,
    nazwy_cech_lokalizacji_nlp,
    wyciagnij_cechy_z_lematow_string,
)


def statystyki_opisu(opis: str | None) -> dict[str, float]:
    """Długość tekstu i liczba tokenów"""

    if opis is None or not isinstance(opis, str):
        bez_spacji = ""
    else:
        bez_spacji = opis.strip()
    slowa = re.findall(r"\w+", bez_spacji, flags=re.UNICODE)
    return {
        "dlugosc_opisu_znaki": float(len(bez_spacji)),
        "liczba_slow_opisu": float(len(slowa)),
    }


def nazwy_kolumn_cech_tekstowych() -> tuple[str, ...]:
    """Wszystkie nazwy kolumn generowanych przez :func:`wyciagnij_cechy_nlp`"""

    return nazwy_cech_lokalizacji_nlp() + (
        "dlugosc_opisu_znaki",
        "liczba_slow_opisu",
    )


def wyciagnij_cechy_nlp(opis: str | None) -> dict[str, float]:
    """Łączy statystyki opisu ze zmiennymi morze/centrum"""

    out: dict[str, float] = {}
    out.update(statystyki_opisu(opis))
    out.update(cechy_lokalizacji_z_korzeni(opis))
    return out


def wyciagnij_cechy_slownikowe(opis: str | None) -> dict[str, float]:


    return wyciagnij_cechy_nlp(opis)


def trafienia_slow_kluczowych(opis: str | None) -> dict[str, bool]:
    """Podgląd wartości logicznych dla morze/centrum """

    raw = cechy_lokalizacji_z_korzeni(opis)
    return {k: bool(v) for k, v in raw.items()}


# Aliasy pod starszy kod / English
extract_dictionary_features = wyciagnij_cechy_nlp
text_feature_columns = nazwy_kolumn_cech_tekstowych
KEYWORD_GROUPS = {}  # tryb dopasowania substring — wycofany na rzecz NLP


__all__ = [
    "statystyki_opisu",
    "nazwy_kolumn_cech_tekstowych",
    "wyciagnij_cechy_nlp",
    "wyciagnij_cechy_slownikowe",
    "trafienia_slow_kluczowych",
    "wyciagnij_cechy_z_lematow_string",
]
