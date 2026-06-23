"""Testy logów audytu"""

from pathlib import Path

import pytest

from repozytorium.db.logi_audytu import RejestrAudytu


@pytest.fixture
def rejestr(tmp_path: Path):
    return RejestrAudytu(sciezka_bazy=tmp_path / "test_app.sqlite3")


def test_schemat_tworzy_tabele(rejestr, tmp_path: Path):
    import sqlite3

    with sqlite3.connect(rejestr.sciezka_bazy) as conn:
        tabele = {
            w[0]
            for w in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
    assert "logi_audytu" in tabele
    assert tmp_path.joinpath("test_app.sqlite3").exists()


def test_zapis_i_odczyt(rejestr):
    rejestr.zapisz("szacowanie", "RF=120000 EUR")
    wpisy = rejestr.pobierz(limit=5)
    assert len(wpisy) == 1
    assert wpisy[0].akcja == "szacowanie"
    assert "120000" in wpisy[0].szczegoly
    assert wpisy[0].uzytkownik


def test_wyczysc(rejestr):
    rejestr.zapisz("test", "x")
    usuniete = rejestr.wyczysc()
    assert usuniete == 1
    assert rejestr.pobierz() == []
