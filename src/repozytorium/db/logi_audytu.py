"""Rejestr audytu czyli kto, kiedy i jakie akcje wykonał w aplikacji

Wpisy trafiają do tabeli ``logi_audytu`` w ``data/app.sqlite3``
Przy pierwszym uruchomieniu baza i tabela są tworzone automatycznie

:author: Stanisław Kwak
:license: MIT
"""

from __future__ import annotations

import getpass
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from repozytorium.paths import app_database_path


@dataclass
class WpisAudytu:
    """Pojedynczy wpis logu audytu"""

    id: int
    czas: str
    uzytkownik: str
    akcja: str
    szczegoly: str


class RejestrAudytu:
    """Zapis i odczyt logów audytu w SQL"""

    def __init__(self, sciezka_bazy: str | Path | None = None) -> None:
        self.sciezka_bazy = Path(sciezka_bazy) if sciezka_bazy else app_database_path()
        self.sciezka_bazy.parent.mkdir(parents=True, exist_ok=True)
        self._utworz_schemat()

    @staticmethod
    def _uzytkownik_systemu() -> str:
        """Identyfikator użytkownika OS"""

        try:
            return getpass.getuser() or "nieznany"
        except OSError:
            return "nieznany"

    def _utworz_schemat(self) -> None:
        """Tworzy tabelę ``logi_audytu``, jeśli jeszcze nie istnieje"""

        with sqlite3.connect(self.sciezka_bazy) as polaczenie:
            polaczenie.execute(
                """
                CREATE TABLE IF NOT EXISTS logi_audytu (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    czas TEXT NOT NULL,
                    uzytkownik TEXT NOT NULL,
                    akcja TEXT NOT NULL,
                    szczegoly TEXT NOT NULL DEFAULT ''
                )
                """
            )
            polaczenie.commit()

    def zapisz(self, akcja: str, szczegoly: str = "") -> None:
        """Dodaje wpis audytu

        :param akcja: Krótka nazwa zdarzenia, np. ``szacowanie``
        :param szczegoly: Dodatkowy opis tekstowy bez danych wrażliwych
        """

        czas = datetime.now(timezone.utc).isoformat(timespec="seconds")
        uzytkownik = self._uzytkownik_systemu()
        with sqlite3.connect(self.sciezka_bazy) as polaczenie:
            polaczenie.execute(
                """
                INSERT INTO logi_audytu (czas, uzytkownik, akcja, szczegoly)
                VALUES (?, ?, ?, ?)
                """,
                (czas, uzytkownik, akcja, szczegoly[:2000]),
            )
            polaczenie.commit()

    def pobierz(self, limit: int = 100) -> list[WpisAudytu]:
        """Zwraca ostatnie wpisy posortowane malejąco po ``id``

        :param limit: Maksymalna liczba rekordów
        """

        with sqlite3.connect(self.sciezka_bazy) as polaczenie:
            wiersze = polaczenie.execute(
                """
                SELECT id, czas, uzytkownik, akcja, szczegoly
                FROM logi_audytu
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [
            WpisAudytu(
                id=int(w[0]),
                czas=str(w[1]),
                uzytkownik=str(w[2]),
                akcja=str(w[3]),
                szczegoly=str(w[4]),
            )
            for w in wiersze
        ]

    def wyczysc(self) -> int:
        """Usuwa wszystkie wpisy audytu

        :returns: Liczba usuniętych rekordów
        """

        with sqlite3.connect(self.sciezka_bazy) as polaczenie:
            kursor = polaczenie.execute("DELETE FROM logi_audytu")
            polaczenie.commit()
            return int(kursor.rowcount)
