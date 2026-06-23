"""Wczytywanie oczyszczonych ogłoszeń z bazy SQL do ``pandas.DataFrame``

:author: Stanisław Kwak
:license: MIT
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from repozytorium.data import schema
from repozytorium.paths import clean_ads_db_path


class LadowarkaDanych:
    """Czyta tabelę ``clean_ads`` i udostępnia ją jako ramkę danych

    Klasa nie modyfikuje bazy źródłowej tylko wykonuje wyłącznie odczyt. Dzięki
    parametrowi ``sciezka_bazy`` można wskazać dowolny plik SQL, co jest przydatne
    w testach do podania bazy tymczasowej
    """

    def __init__(self, sciezka_bazy: str | Path | None = None) -> None:
        """Tworzy ładowarkę

        :param sciezka_bazy: Ścieżka do pliku bazy. Gdy ``None`` — domyślna
            lokalizacja ``kv_clean.sqlite3`` w katalogu projektu
        """

        self.sciezka_bazy = Path(sciezka_bazy) if sciezka_bazy else clean_ads_db_path()

    def wczytaj_tabel(self, nazwa_tabeli: str = "clean_ads") -> pd.DataFrame:
        """Zwraca całą tabelę ogłoszeń bez dodatkowych przekształceń

        :param nazwa_tabeli: Nazwa tabeli do odczytu
        :raises FileNotFoundError: Gdy plik bazy nie istnieje
        :returns: Ramka danych ze wszystkimi kolumnami tabeli
        """

        if not self.sciezka_bazy.exists():
            raise FileNotFoundError(
                f"Nie znaleziono bazy danych: {self.sciezka_bazy}"
            )
        with sqlite3.connect(str(self.sciezka_bazy)) as polaczenie:
            return pd.read_sql_query(f"SELECT * FROM {nazwa_tabeli}", polaczenie)

    def wczytaj_do_modelu(self, nazwa_tabeli: str = "clean_ads") -> pd.DataFrame:
        """Zwraca dane przefiltrowane pod trening modelu

        Usuwa wiersze bez ceny oraz odcina ceny poza sensownym zakresem
        (:data:`~repozytorium.data.schema.MIN_CENA`–
        :data:`~repozytorium.data.schema.MAX_CENA`), aby ograniczyć wpływ
        błędnych ogłoszeń na model

        :param nazwa_tabeli: Nazwa tabeli do odczytu
        :returns: Oczyszczona ramka danych
        """

        df = self.wczytaj_tabel(nazwa_tabeli)
        df = df.dropna(subset=[schema.KOLUMNA_CELU])
        df = df[
            (df[schema.KOLUMNA_CELU] >= schema.MIN_CENA)
            & (df[schema.KOLUMNA_CELU] <= schema.MAX_CENA)
        ]
        return df.reset_index(drop=True)
