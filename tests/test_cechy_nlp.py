"""Testy cech NLP"""

import pytest

from repozytorium.features.cechy_lokalizacji_nlp import (
    cechy_lokalizacji_z_korzeni,
    wyciagnij_cechy_z_lematow_string,
)


@pytest.mark.parametrize(
    "opis, oczekiwane_morze, oczekiwane_centrum",
    [
        ("meri rand supelrand mere ääres", True, False),
        ("kesklinn ja vanalinn kesklinnas", False, True),
        ("", False, False),
        (None, False, False),
    ],
    ids=["morze_rand", "kesklinn_vanalinn", "pusty", "none"],
)
def test_cechy_lokalizacji_z_korzeni(opis, oczekiwane_morze, oczekiwane_centrum):
    wynik = cechy_lokalizacji_z_korzeni(opis)
    assert wynik["nlp_bliskosc_morza"] == float(oczekiwane_morze)
    assert wynik["nlp_centrum_miasta"] == float(oczekiwane_centrum)


def test_cechy_z_lematow():
    lematy = "meri rand kesklinn"
    w = wyciagnij_cechy_z_lematow_string(lematy)
    assert w["nlp_bliskosc_morza"] == 1.0
    assert w["nlp_centrum_miasta"] == 1.0
