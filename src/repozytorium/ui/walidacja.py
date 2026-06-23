"""Walidacja pól formularza w aplikacji

:author: Stanisław Kwak
:license: MIT
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from repozytorium.ui import teksty_pl as T


@dataclass
class WynikWalidacji:
    """Wynik sprawdzenia pojedynczego pola"""

    poprawne: bool
    wartosc: float | int | None = None
    komunikat: str = ""


class WalidatorFormularza:
    """Sprawdza i normalizuje dane wprowadzone w interfejsie Flet"""

    _WZOR_LICZBY = re.compile(r"^\s*(\d+(?:[.,]\d+)?)\s*$")

    ZAKRESY: dict[str, tuple[float, float]] = {
        "powierzchnia_m2": (5.0, 2_000.0),
        "liczba_pokoi": (1.0, 20.0),
        "liczba_sypialni": (0.0, 15.0),
        "pietro": (-2.0, 60.0),
        "liczba_pieter": (1.0, 60.0),
        "rok_budowy": (1800.0, 2030.0),
        "cena_oferty": (10_000.0, 2_000_000.0),
    }

    def parsuj_liczbe(
        self,
        tekst: str | None,
        nazwa_pola: str,
        wymagane: bool = False,
        calkowite: bool = False,
    ) -> WynikWalidacji:
        """Parsuje tekst do liczby z opcjonalną kontrolą zakresu

        :param tekst: Wartość z pola tekstowego
        :param nazwa_pola: Klucz do :data:`ZAKRESY`; pusty oznacza brak zakresu
        :param wymagane: Czy puste pole jest błędem
        :param calkowite: Czy wynik ma być zaokrąglony do int
        """

        if tekst is None or not str(tekst).strip():
            if wymagane:
                return WynikWalidacji(False, komunikat="Pole wymagane.")
            return WynikWalidacji(True, None)

        dopasowanie = self._WZOR_LICZBY.match(str(tekst))
        if not dopasowanie:
            return WynikWalidacji(
                False,
                komunikat="Dozwolone są wyłącznie cyfry (np. 48 lub 48,5).",
            )

        wartosc = float(dopasowanie.group(1).replace(",", "."))
        if calkowite:
            wartosc = int(round(wartosc))

        if nazwa_pola in self.ZAKRESY:
            dol, gora = self.ZAKRESY[nazwa_pola]
            if wartosc < dol or wartosc > gora:
                return WynikWalidacji(
                    False,
                    wartosc=wartosc,
                    komunikat=f"Wartość poza zakresem {dol:g}–{gora:g}.",
                )

        return WynikWalidacji(True, wartosc)

    def zbuduj_slownik_wejscia(self, pola: dict[str, object]) -> tuple[dict, list[str]]:
        """Buduje słownik danych dla modelu i listę błędów walidacji

        :param pola: Słownik wartości z formularza
        :returns: Słownik danych modelu i lista komunikatów błędów
        """

        bledy: list[str] = []
        dane: dict[str, object] = {}

        mapowanie_liczbowe = {
            "powierzchnia_m2": ("powierzchnia_m2", False, False),
            "liczba_pokoi": ("liczba_pokoi", False, True),
            "liczba_sypialni": ("liczba_sypialni", False, True),
            "pietro": ("pietro", False, True),
            "liczba_pieter": ("liczba_pieter", False, True),
            "rok_budowy": ("rok_budowy", False, True),
        }

        for klucz_form, (klucz_model, wymagane, calkowite) in mapowanie_liczbowe.items():
            wynik = self.parsuj_liczbe(
                pola.get(klucz_form),
                klucz_model,
                wymagane=wymagane,
                calkowite=calkowite,
            )
            if not wynik.poprawne:
                bledy.append(f"{klucz_form}: {wynik.komunikat}")
            elif wynik.wartosc is not None:
                dane[klucz_model] = wynik.wartosc

        for klucz in ("stan", "klasa_energetyczna"):
            wartosc = pola.get(klucz)
            if wartosc not in (None, ""):
                dane[klucz] = wartosc

        for klucz in ("nlp_bliskosc_morza", "nlp_centrum_miasta"):
            wartosc = pola.get(klucz)
            if wartosc in ("1", "0", 1, 0, 1.0, 0.0):
                dane[klucz] = float(wartosc)

        pokoje = dane.get("liczba_pokoi")
        sypialnie = dane.get("liczba_sypialni")
        if pokoje is not None and sypialnie is not None and pokoje <= sypialnie:
            bledy.append(T.BLAD_POKOI_SYPIALNIE)

        if not dane:
            bledy.append(T.BLAD_BRAK_PARAMETROW)

        return dane, bledy
