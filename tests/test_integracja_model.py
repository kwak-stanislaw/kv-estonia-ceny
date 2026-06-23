"""Test integracyjny: trening na próbce + predykcja."""

from pathlib import Path

import joblib
import pandas as pd
import pytest

from repozytorium.data.feature_engineering import BudowniczyCech
from repozytorium.model.predykcja import Estymator
from repozytorium.model.trening import PakietModeli, TrenerModelu


@pytest.fixture
def probka_df():
    """ramka z kolumnami"""

    return pd.DataFrame(
        {
            "cena": [120_000, 95_000, 150_000, 110_000, 200_000] * 4,
            "powierzchnia_m2": [45, 38, 62, 50, 80] * 4,
            "liczba_pokoi": [2, 2, 3, 2, 4] * 4,
            "liczba_sypialni": [1, 1, 2, 1, 3] * 4,
            "pietro": [3, 1, 5, 2, 0] * 4,
            "liczba_pieter": [9, 5, 12, 8, 4] * 4,
            "rok_budowy": [2010, 1985, 2020, 2005, 2018] * 4,
            "stan": ["Bardzo dobry", "Do remontu", "Nowy / Deweloperski", "Po remoncie", "Standard średni"] * 4,
            "forma_wlasnosci": ["Pełna własność"] * 20,
            "klasa_energetyczna": ["b", "c", "a", "d", "e"] * 4,
            "opis": [
                "meri rand",
                "kesklinn",
                "tavaline korter",
                "rand ja meri",
                "vanalinn",
            ] * 4,
        }
    )


def test_trening_i_predykcja(probka_df, tmp_path: Path):
    trener = TrenerModelu(losowość=0)
    pakiet = trener.trenuj(probka_df)
    sciezka = tmp_path / "test_bundle.joblib"
    joblib.dump(pakiet, sciezka)

    est = Estymator(sciezka=sciezka)
    wynik = est.oszacuj(
        {
            "powierzchnia_m2": 50,
            "liczba_pokoi": 2,
            "nlp_bliskosc_morza": 1,
            "stan": "Bardzo dobry",
        }
    )
    assert wynik.liniowy.punkt > 0
    assert wynik.random_forest.punkt > 0
    assert wynik.random_forest.dol <= wynik.random_forest.punkt <= wynik.random_forest.gora


def test_ocena_oferty(probka_df, tmp_path: Path):
    pakiet = TrenerModelu(losowość=0).trenuj(probka_df)
    sciezka = tmp_path / "bundle.joblib"
    joblib.dump(pakiet, sciezka)
    est = Estymator(sciezka=sciezka)
    ocena, _ = est.ocen_oferte({"powierzchnia_m2": 50}, 50_000)
    assert ocena in ("korzystna", "przeciętna", "za wysoka")


def test_wiersz_z_wejscia_nlp():
    wiersz = BudowniczyCech().wiersz_z_wejscia(
        {"nlp_bliskosc_morza": 1, "nlp_centrum_miasta": 0}
    )
    assert wiersz["nlp_bliskosc_morza"].iloc[0] == 1.0
    assert wiersz["nlp_centrum_miasta"].iloc[0] == 0.0
