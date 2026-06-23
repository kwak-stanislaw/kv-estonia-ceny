"""Testy walidacji GUI"""

import pytest

from repozytorium.ui import teksty_pl as T
from repozytorium.ui.walidacja import WalidatorFormularza


@pytest.fixture
def walidator():
    return WalidatorFormularza()


@pytest.mark.parametrize(
    "tekst, nazwa, oczekiwane",
    [
        ("52,5", "powierzchnia_m2", 52.5),
        ("3", "liczba_pokoi", 3),
        ("", "powierzchnia_m2", None),
        ("abc", "powierzchnia_m2", "blad"),
        ("1", "powierzchnia_m2", "blad"),
    ],
    ids=["przecinek", "calkowite", "puste", "tekst", "za_male"],
)
def test_parsuj_liczbe(walidator, tekst, nazwa, oczekiwane):
    wynik = walidator.parsuj_liczbe(tekst, nazwa)
    if oczekiwane == "blad":
        assert not wynik.poprawne
    else:
        assert wynik.poprawne
        assert wynik.wartosc == oczekiwane


def test_zbuduj_slownik_wejscia(walidator):
    dane, bledy = walidator.zbuduj_slownik_wejscia(
        {
            "powierzchnia_m2": "65",
            "liczba_pokoi": "3",
            "nlp_bliskosc_morza": "1",
        }
    )
    assert not bledy
    assert dane["powierzchnia_m2"] == 65
    assert dane["nlp_bliskosc_morza"] == 1.0


def test_zbuduj_slownik_pusty_formularz(walidator):
    dane, bledy = walidator.zbuduj_slownik_wejscia({})
    assert not dane
    assert len(bledy) == 1


@pytest.mark.parametrize(
    "pokoje, sypialnie, poprawne",
    [
        ("4", "3", True),
        ("3", "3", False),
        ("2", "3", False),
        ("5", "", True),
        ("", "2", True),
    ],
    ids=["ok", "rowne", "za_malo_pokoi", "tylko_pokoje", "tylko_sypialnie"],
)
def test_pokoi_wieksze_niz_sypialnie(walidator, pokoje, sypialnie, poprawne):
    dane, bledy = walidator.zbuduj_slownik_wejscia(
        {
            "powierzchnia_m2": "50",
            "liczba_pokoi": pokoje,
            "liczba_sypialni": sypialnie,
        }
    )
    if poprawne:
        assert T.BLAD_POKOI_SYPIALNIE not in bledy
        assert dane.get("powierzchnia_m2") == 50
    else:
        assert T.BLAD_POKOI_SYPIALNIE in bledy
