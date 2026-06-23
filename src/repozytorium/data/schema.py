"""
Trzymanie nazw kolumn w jednym miejscu eliminuje rozjazd między modułem
treningu oraz interfejsem 

:author: Stanisław Kwak
:license: MIT
"""

from __future__ import annotations

#: Nazwa kolumny celu
KOLUMNA_CELU: str = "cena"

#: Kolumna z tekstem opisu ogłoszenia
KOLUMNA_OPISU: str = "opis"

#: Numeryczne cechy strukturalne pobierane wprost z bazy
CECHY_NUMERYCZNE: tuple[str, ...] = (
    "powierzchnia_m2",
    "liczba_pokoi",
    "liczba_sypialni",
    "pietro",
    "liczba_pieter",
    "rok_budowy",
)

#: Kategoryczne cechy strukturalne kodowane one-hot w potoku modelu
CECHY_KATEGORYCZNE: tuple[str, ...] = (
    "stan",
    "forma_wlasnosci",
    "klasa_energetyczna",
)

#: Cechy inżynierowane z tekstu opisu
CECHY_TEKSTOWE: tuple[str, ...] = (
    "dlugosc_opisu_znaki",
    "liczba_slow_opisu",
    "nlp_bliskosc_morza",
    "nlp_centrum_miasta",
)

#: Pełna lista predyktorów wykorzystywanych przez model
WSZYSTKIE_CECHY: tuple[str, ...] = (
    CECHY_NUMERYCZNE + CECHY_TEKSTOWE + CECHY_KATEGORYCZNE
)

#: Cechy traktowane numerycznie w potoku
CECHY_NUMERYCZNE_PELNE: tuple[str, ...] = CECHY_NUMERYCZNE + CECHY_TEKSTOWE

#: Rozsądne granice ceny — odcinają błędne ogłoszenia
MIN_CENA: float = 10_000.0
MAX_CENA: float = 2_000_000.0
