"""Wykorzystanie wytrenowanego pakietu modeli: oszacowania, przedziały, ocena oferty

:author: Stanisław Kwak
:license: MIT
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np

from repozytorium.data.feature_engineering import BudowniczyCech
from repozytorium.paths import default_model_bundle_path

#: Mnożnik kwantyla normalnego dla około 80% przedziału predykcyjnego
Z_80 = 1.2816

#: Etykiety oceny atrakcyjności podanej ceny
OCENA_KORZYSTNA = "korzystna"
OCENA_PRZECIETNA = "przeciętna"
OCENA_WYSOKA = "za wysoka"


@dataclass
class OszacowanieModelu:
    """Wynik pojedynczego modelu czyli punkt i przedział w euro"""

    punkt: float
    dol: float
    gora: float


@dataclass
class WynikOszacowania:
    """Łączny wynik oszacowania z obu modeli"""

    liniowy: OszacowanieModelu
    random_forest: OszacowanieModelu

    @property
    def srednia_punktowa(self) -> float:
        """Średnia oszacowań punktowych obu modeli"""

        return float((self.liniowy.punkt + self.random_forest.punkt) / 2.0)


class BrakModeluError(RuntimeError):
    """Podnoszony, gdy pakiet modeli nie został jeszcze wytrenowany lubzapisany"""


class Estymator:
    """Wczytuje pakiet modeli i udostępnia oszacowania ceny"""

    def __init__(self, pakiet=None, sciezka: str | Path | None = None) -> None:
        """Wczytuje pakiet modeli z pamięci lub z pliku joblib

        :param pakiet: Gotowy ``PakietModeli`` albo ``None`` — wtedy wczytanie z dysku
        :param sciezka: Ścieżka pliku ``.joblib``; gdy ``None`` — domyślna
        """

        self.budowniczy = BudowniczyCech()
        if pakiet is not None:
            self.pakiet = pakiet
        else:
            cel = Path(sciezka) if sciezka else default_model_bundle_path()
            if not cel.exists():
                raise BrakModeluError(
                    f"Nie znaleziono pakietu modeli: {cel}. "
                    "Uruchom: python -m repozytorium.model.trening"
                )
            self.pakiet = joblib.load(cel)

    @staticmethod
    def czy_dostepny(sciezka: str | Path | None = None) -> bool:
        """Sprawdza czy plik pakietu modeli istnieje

        :param sciezka: Ścieżka pliku; gdy ``None`` — domyślna
        :returns: ``True`` jeśli pakiet można wczytać
        """

        cel = Path(sciezka) if sciezka else default_model_bundle_path()
        return cel.exists()

    def _przedzial(self, punkt: float, sigma_log: float) -> tuple[float, float]:
        """Przedział z odchylenia reszt w skali log"""

        log_p = np.log1p(max(punkt, 0.0))
        dol = float(np.expm1(log_p - Z_80 * sigma_log))
        gora = float(np.expm1(log_p + Z_80 * sigma_log))
        return max(dol, 0.0), max(gora, 0.0)

    def oszacuj(self, dane: dict[str, object]) -> WynikOszacowania:
        """Zwraca oszacowania obu modeli wraz z przedziałami

        :param dane: Słownik parametrów nieruchomości wraz z opisem
        :returns: :class:`WynikOszacowania` z wynikami obu modeli
        """

        X = self.budowniczy.wiersz_z_wejscia(dane)

        punkt_lin = float(self.pakiet.model_liniowy.predict(X)[0])
        punkt_las = float(self.pakiet.model_las.predict(X)[0])

        dol_lin, gora_lin = self._przedzial(punkt_lin, self.pakiet.sigma_log["liniowy"])
        dol_las, gora_las = self._przedzial(punkt_las, self.pakiet.sigma_log["las"])

        return WynikOszacowania(
            liniowy=OszacowanieModelu(punkt_lin, dol_lin, gora_lin),
            random_forest=OszacowanieModelu(punkt_las, dol_las, gora_las),
        )

    def ocen_oferte(
        self, dane: dict[str, object], cena_oferty: float
    ) -> tuple[str, WynikOszacowania]:
        """Ocenia, czy podana cena jest korzystna, przeciętna czy za wysoka

        Punktem odniesienia jest model random forest i jego przedział: cena
        poniżej dolnej granicy to cena korzystna, powyżej górnej — cena zawyżona

        :param dane: Parametry nieruchomości.
        :param cena_oferty: Cena z oferty do oceny w euro
        :returns: Etykieta oceny i wynik oszacowania
        """

        wynik = self.oszacuj(dane)
        odniesienie = wynik.random_forest
        if cena_oferty < odniesienie.dol:
            ocena = OCENA_KORZYSTNA
        elif cena_oferty > odniesienie.gora:
            ocena = OCENA_WYSOKA
        else:
            ocena = OCENA_PRZECIETNA
        return ocena, wynik
