"""dołączanie statystyk opisu

:author: Stanisław Kwak
:license: MIT
"""

from __future__ import annotations

import pandas as pd

from repozytorium.data import schema
from repozytorium.features.text_keywords import wyciagnij_cechy_nlp


class BudowniczyCech:
    """Przekształca nietykane ogłoszenia"""

    def dodaj_cechy_tekstowe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Dodaje kolumny cech tekstowych

        Jeśli kolumny :data:`schema.CECHY_TEKSTOWE` są już w ramce po skrypcie
        ``wzbogac_baze_nlp``, opisy nie są przeliczane ponownie
        """

        df = df.copy()
        if all(k in df.columns for k in schema.CECHY_TEKSTOWE):
            return df

        opisy = df.get(schema.KOLUMNA_OPISU, pd.Series([None] * len(df)))
        cechy = opisy.apply(wyciagnij_cechy_nlp)
        cechy_df = pd.DataFrame(list(cechy), index=df.index)
        for kolumna in schema.CECHY_TEKSTOWE:
            df[kolumna] = cechy_df.get(kolumna, 0.0)
        return df

    def przygotuj_X_y(
        self, df: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.Series]:
        """Buduje macierz predyktorów ``X`` i wektor celu ``y``

        :param df: Oczyszczone ogłoszenia z
            :meth:`~repozytorium.data.loader.LadowarkaDanych.wczytaj_do_modelu`
        :returns: Macierz ``X`` i wektor ``y`` z kolumnami :data:`schema.WSZYSTKIE_CECHY`
            oraz :data:`schema.KOLUMNA_CELU`
        """

        wzbogacone = self.dodaj_cechy_tekstowe(df)
        X = wzbogacone[list(schema.WSZYSTKIE_CECHY)].copy()
        y = wzbogacone[schema.KOLUMNA_CELU].astype(float)
        return X, y

    def wiersz_z_wejscia(self, dane: dict[str, object]) -> pd.DataFrame:
        """Tworzy jednowierszową ramkę cech z danych podanych przez użytkownika

        Cechy lokalizacyjne ``nlp_*`` podaje użytkownik jako tak lub nie
        Brakujące pola uzupełni imputer

        :param dane: Słownik z podzbiorem cech, w tym opcjonalnie ``nlp_*``
        :returns: Ramka o jednym wierszu z kolumnami :data:`schema.WSZYSTKIE_CECHY`
        """

        wiersz: dict[str, object] = {nazwa: None for nazwa in schema.WSZYSTKIE_CECHY}

        for nazwa in schema.CECHY_NUMERYCZNE + schema.CECHY_KATEGORYCZNE:
            if nazwa in dane and dane[nazwa] not in (None, ""):
                wiersz[nazwa] = dane[nazwa]

        for nazwa in schema.CECHY_TEKSTOWE:
            if nazwa in dane and dane[nazwa] not in (None, ""):
                wiersz[nazwa] = float(dane[nazwa])

        return pd.DataFrame([wiersz], columns=list(schema.WSZYSTKIE_CECHY))
