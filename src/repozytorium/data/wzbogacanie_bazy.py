"""cechy wyciągnięte z opisu

Zmienne ``nlp_bliskosc_morza``, ``nlp_centrum_miasta`` liczone są **batchowo**

:author: Stanisław Kwak
:license: MIT
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from repozytorium.data import schema
from repozytorium.data.loader import LadowarkaDanych
from repozytorium.features.text_keywords import wyciagnij_cechy_nlp
from repozytorium.paths import clean_ads_db_path


class WzbogacaczBazy:
    """Dopisuje kolumny do tabeli ``clean_ads``"""

    def __init__(self, sciezka_bazy: str | Path | None = None) -> None:
        self.sciezka_bazy = Path(sciezka_bazy) if sciezka_bazy else clean_ads_db_path()

    def _kolumny_w_bazie(self, polaczenie: sqlite3.Connection) -> set[str]:
        wiersze = polaczenie.execute("PRAGMA table_info(clean_ads)").fetchall()
        return {w[1] for w in wiersze}

    def _dodaj_kolumny_jesli_brak(self, polaczenie: sqlite3.Connection) -> None:
        istniejace = self._kolumny_w_bazie(polaczenie)
        for kolumna in schema.CECHY_TEKSTOWE:
            if kolumna not in istniejace:
                polaczenie.execute(
                    f"ALTER TABLE clean_ads ADD COLUMN {kolumna} REAL"
                )

    def wzbogac(self, nazwa_tabeli: str = "clean_ads") -> dict[str, float]:
        """Liczy cechy dla wszystkich wierszy i zapisuje je w bazie

        :returns: Statystyki morze i centrum
        """

        df = LadowarkaDanych(self.sciezka_bazy).wczytaj_tabel(nazwa_tabeli)
        opisy = df.get(schema.KOLUMNA_OPISU, pd.Series([None] * len(df)))
        cechy = opisy.apply(wyciagnij_cechy_nlp)
        cechy_df = pd.DataFrame(list(cechy), index=df.index)

        with sqlite3.connect(str(self.sciezka_bazy)) as polaczenie:
            self._dodaj_kolumny_jesli_brak(polaczenie)
            for idx, wiersz in cechy_df.iterrows():
                url = df.at[idx, "url"]
                polaczenie.execute(
                    f"""
                    UPDATE {nazwa_tabeli}
                    SET {", ".join(f"{k} = ?" for k in schema.CECHY_TEKSTOWE)}
                    WHERE url = ?
                    """,
                    (*[float(wiersz[k]) for k in schema.CECHY_TEKSTOWE], url),
                )

        return {
            "rekordow": float(len(df)),
            "udzial_morze": float(cechy_df["nlp_bliskosc_morza"].mean()),
            "udzial_centrum": float(cechy_df["nlp_centrum_miasta"].mean()),
        }


def main() -> None:
    """dodanie do ``kv_clean.sqlite3`` nowych kolumn"""

    stat = WzbogacaczBazy().wzbogac()
    print(f"Zaktualizowano {int(stat['rekordow'])} ogłoszeń.")
    print(f"  dostęp do morza (w opisie): {stat['udzial_morze']*100:.1f}%")
    print(f"  centrum miasta (w opisie): {stat['udzial_centrum']*100:.1f}%")


if __name__ == "__main__":
    main()
