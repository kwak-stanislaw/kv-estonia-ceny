"""Główna aplikacja Flet szacowanie ceny nieruchomości KV.ee

:author: Stanisław Kwak
:license: MIT
"""

from __future__ import annotations

import flet as ft

from repozytorium.db.logi_audytu import RejestrAudytu
from repozytorium.model.predykcja import (
    BrakModeluError,
    Estymator,
    OCENA_KORZYSTNA,
    OCENA_PRZECIETNA,
    OCENA_WYSOKA,
)
from repozytorium.ui import teksty_pl as T
from repozytorium.ui.walidacja import WalidatorFormularza

# Kolory i styl
_KOLOR_TLO = "#0f172a"
_KOLOR_KARTA = "#1e293b"
_KOLOR_OBRYS = "#334155"
_KOLOR_AKCENT = "#38bdf8"
_KOLOR_SUKCES = "#4ade80"
_KOLOR_OSTRZEZENIE = "#fbbf24"
_KOLOR_BLAD = "#f87171"
_KOLOR_TEKST = "#f1f5f9"
_KOLOR_TEKST_DRUGI = "#94a3b8"
_ODSTEP_POLA = 16
_PROMIEN = 8


def _formatuj_cene(wartosc: float) -> str:
    """Formatuje cenę w euro z separatorem tysięcy"""

    return f"{max(wartosc, 0.0):,.0f} €".replace(",", " ")


def _etykieta_oceny(ocena: str) -> tuple[str, str]:
    """Zwraca tekst i kolor dla oceny oferty"""

    if ocena == OCENA_KORZYSTNA:
        return T.OCENA_TEKST_KORZYSTNA, _KOLOR_SUKCES
    if ocena == OCENA_WYSOKA:
        return T.OCENA_TEKST_WYSOKA, _KOLOR_BLAD
    return T.OCENA_TEKST_PRZECIETNA, _KOLOR_AKCENT


class AplikacjaSzacowania:
    """Zarządza widokiem: start, o aplikacji, szacowanie"""

    OPCJE_STAN = [
        "Nowy / Deweloperski",
        "Standard średni",
        "Bardzo dobry",
        "Do remontu",
        "Po remoncie",
    ]
    OPCJE_ENERGIA = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "Nieokreślona",
    ]

    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.walidator = WalidatorFormularza()
        self.rejestr_audytu = RejestrAudytu()
        self.estymator: Estymator | None = None

        self._pola_liczbowe: dict[str, ft.TextField] = {}
        self._dropdowny: dict[str, ft.Dropdown] = {}
        self._pole_cena_oferty: ft.TextField | None = None
        self._panel_wynik: ft.Container | None = None
        self._panel_ocena: ft.Container | None = None
        self._snackbar: ft.SnackBar | None = None
        self._kontener_widoku: ft.Column | None = None
        self._widoki: dict[str, ft.Control] = {}

    def _pokaz_trase(self, trasa: str) -> None:
        """Przełącza widok po nazwie trasy"""

        if trasa not in self._widoki:
            budownicze = {
                "start": self._buduj_widok_startowy,
                "o_aplikacji": self._buduj_widok_o_aplikacji,
                "szacowanie": self._buduj_widok_szacowania,
            }
            self._widoki[trasa] = budownicze[trasa]()
        self._pokaz_widok(self._widoki[trasa])

    def _inicjalizuj_estymator(self) -> bool:
        """Próbuje wczytać pakiet modeli; zwraca False gdy brak pliku"""

        try:
            self.estymator = Estymator()
            return True
        except BrakModeluError:
            self.estymator = None
            return False

    def _pokaz_widok(self, zawartosc: ft.Control) -> None:
        """Podmienia główną zawartość strony"""

        if self._kontener_widoku is None:
            return
        self._kontener_widoku.controls.clear()
        self._kontener_widoku.controls.append(
            ft.Container(content=zawartosc, expand=True)
        )
        self.page.update()

    def _pokaz_snackbar(self, tekst: str, kolor: str = _KOLOR_AKCENT) -> None:
        """Wyświetla krótki komunikat u dołu ekranu"""

        self._snackbar = ft.SnackBar(
            content=ft.Text(tekst, color="#0f172a"),
            bgcolor=kolor,
            duration=3500,
        )
        self.page.overlay.append(self._snackbar)
        self._snackbar.open = True
        self.page.update()

    def _loguj(self, akcja: str, szczegoly: str = "") -> None:
        """Zapisuje zdarzenie w rejestrze audytu SQLite"""

        self.rejestr_audytu.zapisz(akcja, szczegoly)

    def _stopka(self) -> ft.Control:
        """Stopka z autorem, licencją i dyskretnym dostępem do logów"""

        import repozytorium

        return ft.Row(
            [
                ft.Container(
                    content=ft.Text(
                        f"© {repozytorium.__author__} · {repozytorium.__license__}",
                        size=10,
                        color="#475569",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    expand=True,
                    alignment=ft.Alignment.CENTER,
                ),
                ft.IconButton(
                    icon=ft.Icons.RECEIPT_LONG,
                    icon_size=18,
                    icon_color="#475569",
                    tooltip=T.LOGI_AUDYTU_TOOLTIP,
                    on_click=self._otworz_logi_audytu,
                    style=ft.ButtonStyle(padding=4),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _zamknij_dialog(self, dialog: ft.AlertDialog) -> None:
        """Zamyka okno dialogowe logów"""

        dialog.open = False
        self.page.update()

    def _otworz_logi_audytu(self, _e: ft.ControlEvent) -> None:
        """Pokazuje ostatnie wpisy audytu"""

        self._loguj("podglad_logow")

        wpisy = self.rejestr_audytu.pobierz(limit=50)
        if not wpisy:
            lista = ft.Text(T.LOGI_PUSTE, color=_KOLOR_TEKST_DRUGI, italic=True)
        else:
            wiersze: list[ft.Control] = []
            for wpis in wpisy:
                czas = wpis.czas.replace("T", " ")[:19]
                linia = f"{czas} · {wpis.uzytkownik} · {wpis.akcja}"
                if wpis.szczegoly:
                    linia += f" — {wpis.szczegoly}"
                wiersze.append(
                    ft.Text(linia, size=12, color=_KOLOR_TEKST, selectable=True)
                )
            lista = ft.Column(wiersze, spacing=8, scroll=ft.ScrollMode.AUTO)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(T.TYTUL_LOGI_AUDYTU, size=16, weight=ft.FontWeight.W_600),
            content=ft.Container(content=lista, width=480, height=320),
            bgcolor=_KOLOR_KARTA,
            actions=[
                ft.TextButton(
                    T.PRZYCISK_WYCZYSC_LOGI,
                    on_click=lambda e: self._wyczysc_logi_audytu(e, dialog),
                    style=ft.ButtonStyle(color=_KOLOR_TEKST_DRUGI),
                ),
                ft.TextButton(
                    T.PRZYCISK_ZAMKNIJ,
                    on_click=lambda _: self._zamknij_dialog(dialog),
                    style=ft.ButtonStyle(color=_KOLOR_AKCENT),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def _wyczysc_logi_audytu(
        self, _e: ft.ControlEvent, dialog: ft.AlertDialog
    ) -> None:
        """Usuwa wpisy audytu i zamyka okno"""

        usuniete = self.rejestr_audytu.wyczysc()
        self._zamknij_dialog(dialog)
        self._pokaz_snackbar(
            f"{T.LOGI_WYCZYSZCZONO} ({usuniete})",
            _KOLOR_AKCENT,
        )

    def _przycisk_powrotu(self, trasa: str = "start") -> ft.Control:
        """Przycisk powrotu na wskazaną stronę"""

        return ft.TextButton(
            T.PRZYCISK_POWROT,
            icon=ft.Icons.ARROW_BACK,
            on_click=lambda _: self._pokaz_trase(trasa),
            style=ft.ButtonStyle(color=_KOLOR_AKCENT),
        )

    def _karta(self, tytul: str | None, zawartosc: ft.Control) -> ft.Container:
        """Prosta karta sekcji — jednolity padding i obramowanie"""

        elementy: list[ft.Control] = []
        if tytul:
            elementy.append(
                ft.Text(
                    tytul,
                    size=14,
                    weight=ft.FontWeight.W_600,
                    color=_KOLOR_TEKST,
                )
            )
        elementy.append(zawartosc)
        return ft.Container(
            content=ft.Column(elementy, spacing=12),
            padding=_ODSTEP_POLA,
            bgcolor=_KOLOR_KARTA,
            border=ft.Border.all(1, _KOLOR_OBRYS),
            border_radius=_PROMIEN,
        )

    def _styl_pola_wspolny(self) -> dict:
        """Wspólny wygląd pól tekstowych i list rozwijanych"""

        return {
            "border_color": _KOLOR_OBRYS,
            "focused_border_color": _KOLOR_AKCENT,
            "filled": True,
            "fill_color": _KOLOR_OBRYS,
            "color": _KOLOR_TEKST,
            "label_style": ft.TextStyle(color=_KOLOR_TEKST_DRUGI, size=13),
            "text_size": 15,
            "content_padding": ft.Padding.symmetric(horizontal=12, vertical=14),
            "border_radius": _PROMIEN,
            "dense": False,
            "expand": True,
        }

    def _pole_liczbowe(self, etykieta: str, klucz: str, podpowiedz: str) -> ft.TextField:
        """Pole numeryczne — pełna szerokość, bez nachodzenia etykiet"""

        def filtruj(e: ft.ControlEvent) -> None:
            wpis = e.control.value or ""
            oczyszczone = "".join(
                ch for ch in wpis if ch.isdigit() or ch in ".,"
            )
            if oczyszczone != wpis:
                e.control.value = oczyszczone
                e.control.update()

        pole = ft.TextField(
            label=etykieta,
            hint_text=podpowiedz,
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter=ft.InputFilter(
                regex_string=r"[0-9.,]*",
                allow=True,
                replacement_string="",
            ),
            on_change=filtruj,
            **self._styl_pola_wspolny(),
        )
        self._pola_liczbowe[klucz] = pole
        return pole

    def _dropdown(self, etykieta: str, klucz: str, opcje: list[str]) -> ft.Dropdown:
        """Lista rozwijana — ten sam styl i szerokość co pola tekstowe"""

        dd = ft.Dropdown(
            label=etykieta,
            hint_text=T.PODPOWIEDZ_OPCJONALNE,
            options=[ft.dropdown.Option(o) for o in opcje],
            **self._styl_pola_wspolny(),
        )
        self._dropdowny[klucz] = dd
        return dd

    def _dropdown_tak_nie(self, etykieta: str, klucz: str) -> ft.Dropdown:
        """Tak i nie bez  opcji „brak”"""

        dd = ft.Dropdown(
            label=etykieta,
            hint_text=T.PODPOWIEDZ_OPCJONALNE,
            options=[
                ft.dropdown.Option(key="1", text=T.OPCJA_TAK),
                ft.dropdown.Option(key="0", text=T.OPCJA_NIE),
            ],
            **self._styl_pola_wspolny(),
        )
        self._dropdowny[klucz] = dd
        return dd

    def _zbierz_pola(self) -> dict[str, object]:
        """Czyta wartości z formularza"""

        pola: dict[str, object] = {}
        for klucz, pole in self._pola_liczbowe.items():
            if klucz == "cena_oferty":
                continue
            pola[klucz] = pole.value
        for klucz, dd in self._dropdowny.items():
            pola[klucz] = dd.value
        if self._pole_cena_oferty:
            pola["cena_oferty"] = self._pole_cena_oferty.value
        return pola

    def _wypelnij_wynik(self, wynik) -> None:
        """Aktualizuje panel oszacowania"""

        if self._panel_wynik is None:
            return
        self._panel_wynik.content = _panel_wyniku_minimal(wynik)
        if self._panel_wynik.page is not None:
            self._panel_wynik.update()
        elif self.page:
            self.page.update()

    def _wypelnij_ocene(self, ocena: str, wynik) -> None:
        """Aktualizuje panel oceny podanej ceny oferty"""

        if self._panel_ocena is None:
            return
        tekst, kolor = _etykieta_oceny(ocena)
        self._panel_ocena.content = ft.Container(
            content=ft.Text(tekst, size=14, color=kolor, weight=ft.FontWeight.W_500),
            padding=ft.Padding.symmetric(horizontal=12, vertical=10),
            bgcolor=_KOLOR_OBRYS,
            border_radius=_PROMIEN,
        )
        self._panel_ocena.visible = True
        if self._panel_ocena.page is not None:
            self._panel_ocena.update()
        elif self.page:
            self.page.update()

    def _szacuj(self, _e: ft.ControlEvent | None = None) -> None:
        """Obsługa przycisku Szacuj cenę"""

        if self.estymator is None:
            self._loguj("blad", "brak_modelu")
            self._pokaz_snackbar(T.BLAD_BRAK_MODELU, _KOLOR_OSTRZEZENIE)
            return

        dane, bledy = self.walidator.zbuduj_slownik_wejscia(self._zbierz_pola())
        if bledy:
            self._loguj("blad_walidacji", "; ".join(bledy)[:500])
            self._pokaz_snackbar("; ".join(bledy), _KOLOR_BLAD)
            return

        wynik = self.estymator.oszacuj(dane)
        self._wypelnij_wynik(wynik)
        self._loguj(
            "szacowanie",
            (
                f"RF={wynik.random_forest.punkt:.0f} EUR, "
                f"lin={wynik.liniowy.punkt:.0f} EUR, "
                f"param={len(dane)}"
            ),
        )
        self._pokaz_snackbar(T.SUKCES_OBLICZENIO, _KOLOR_SUKCES)

    def _ocen_cene(self, _e: ft.ControlEvent) -> None:
        """Obsługa przycisku oceny podanej ceny"""

        if self.estymator is None:
            self._loguj("blad", "brak_modelu")
            self._pokaz_snackbar(T.BLAD_BRAK_MODELU, _KOLOR_OSTRZEZENIE)
            return

        pola = self._zbierz_pola()
        wynik_ceny = self.walidator.parsuj_liczbe(
            pola.get("cena_oferty"), "cena_oferty", wymagane=True
        )
        if not wynik_ceny.poprawne:
            self._loguj("blad_walidacji", wynik_ceny.komunikat)
            self._pokaz_snackbar(wynik_ceny.komunikat, _KOLOR_BLAD)
            return

        dane, bledy = self.walidator.zbuduj_slownik_wejscia(pola)
        if bledy:
            self._loguj("blad_walidacji", "; ".join(bledy)[:500])
            self._pokaz_snackbar("; ".join(bledy), _KOLOR_BLAD)
            return

        ocena, wynik = self.estymator.ocen_oferte(dane, float(wynik_ceny.wartosc))
        self._wypelnij_wynik(wynik)
        self._wypelnij_ocene(ocena, wynik)
        self._loguj(
            "ocena_oferty",
            f"cena={float(wynik_ceny.wartosc):.0f} EUR, ocena={ocena}",
        )

    def _buduj_widok_startowy(self) -> ft.Control:
        """Ekran powitalny z nawigacją do szacowania i opisu aplikacji"""

        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(height=24),
                    ft.Icon(ft.Icons.APARTMENT, size=64, color=_KOLOR_AKCENT),
                    ft.Text(
                        T.TYTUL_APLIKACJI,
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        T.PODTYTUL_ZRODLO,
                        size=14,
                        color="#64748b",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        T.PODTYTUL_MODELE,
                        size=13,
                        color="#64748b",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=16),
                    ft.Text(
                        T.START_OPIS_KROTKI,
                        size=15,
                        color="#cbd5e1",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=32),
                    ft.ElevatedButton(
                        T.PRZYCISK_DO_SZACOWANIA,
                        icon=ft.Icons.ARROW_FORWARD,
                        on_click=lambda _: self._pokaz_trase("szacowanie"),
                        bgcolor=_KOLOR_AKCENT,
                        color="#0f172a",
                        width=320,
                        style=ft.ButtonStyle(
                            padding=ft.Padding.symmetric(horizontal=24, vertical=16),
                        ),
                    ),
                    ft.OutlinedButton(
                        T.PRZYCISK_O_APLIKACJI,
                        icon=ft.Icons.INFO_OUTLINE,
                        on_click=lambda _: self._pokaz_trase("o_aplikacji"),
                        width=320,
                        style=ft.ButtonStyle(
                            side=ft.BorderSide(1, _KOLOR_AKCENT),
                            color=_KOLOR_AKCENT,
                            padding=ft.Padding.symmetric(horizontal=24, vertical=16),
                        ),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
            padding=24,
            alignment=ft.Alignment.CENTER,
            expand=True,
        )

    def _buduj_widok_o_aplikacji(self) -> ft.Control:
        """Ekran z opisem działania modeli"""

        tresc_md = "\n\n".join(
            [
                T.O_APLIKACJI_WSTEP,
                T.O_APLIKACJI_REGRESJA,
                T.O_APLIKACJI_RF,
                T.O_APLIKACJI_WYNIK,
            ]
        )

        return ft.Column(
            [
                ft.Row(
                    [
                        self._przycisk_powrotu("start"),
                        ft.Text(
                            T.TYTUL_O_APLIKACJI,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            expand=True,
                        ),
                    ],
                ),
                ft.Container(
                    content=ft.Markdown(
                        tresc_md,
                        selectable=True,
                        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    ),
                    padding=20,
                    bgcolor=_KOLOR_KARTA,
                    border_radius=12,
                ),
                ft.ElevatedButton(
                    T.PRZYCISK_DO_SZACOWANIA,
                    icon=ft.Icons.CALCULATE,
                    on_click=lambda _: self._pokaz_trase("szacowanie"),
                    bgcolor=_KOLOR_AKCENT,
                    color="#0f172a",
                ),
            ],
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def _kafel_pola(self, kontrolka: ft.Control) -> ft.Container:
        """Opakowuje pole formularza — pełna szerokość kolumny siatki"""

        return ft.Container(
            content=kontrolka,
            col={"xs": 12, "sm": 6},
            padding=ft.Padding.only(bottom=4),
            expand=True,
        )

    def _formularz(self) -> ft.Control:
        """Buduje sekcję pól wejściowych bez liczby pięter i formy własności"""

        self._pola_liczbowe.clear()
        self._dropdowny.clear()

        self._pole_cena_oferty = self._pole_liczbowe(
            T.ETYKIETA_CENA_OFERTY, "cena_oferty", "np. 125000"
        )

        siatka = ft.ResponsiveRow(
            [
                self._kafel_pola(
                    self._pole_liczbowe(
                        T.ETYKIETA_POWIERZCHNIA,
                        "powierzchnia_m2",
                        T.PODPOWIEDZ_POWIERZCHNIA,
                    )
                ),
                self._kafel_pola(
                    self._pole_liczbowe(
                        T.ETYKIETA_POKOI, "liczba_pokoi", T.PODPOWIEDZ_LICZBA
                    )
                ),
                self._kafel_pola(
                    self._pole_liczbowe(
                        T.ETYKIETA_SYPIALNI, "liczba_sypialni", T.PODPOWIEDZ_LICZBA
                    )
                ),
                self._kafel_pola(
                    self._pole_liczbowe(
                        T.ETYKIETA_PIETRO, "pietro", T.PODPOWIEDZ_LICZBA
                    )
                ),
                self._kafel_pola(
                    self._pole_liczbowe(
                        T.ETYKIETA_ROK_BUDOWY, "rok_budowy", "np. 2015"
                    )
                ),
                self._kafel_pola(
                    self._dropdown(T.ETYKIETA_STAN, "stan", self.OPCJE_STAN)
                ),
                self._kafel_pola(
                    self._dropdown(
                        T.ETYKIETA_KLASA_ENERGETYCZNA,
                        "klasa_energetyczna",
                        self.OPCJE_ENERGIA,
                    )
                ),
                self._kafel_pola(
                    self._dropdown_tak_nie(
                        T.ETYKIETA_DOSTEP_MORZE, "nlp_bliskosc_morza"
                    )
                ),
                self._kafel_pola(
                    self._dropdown_tak_nie(
                        T.ETYKIETA_CENTRUM, "nlp_centrum_miasta"
                    )
                ),
            ],
            spacing=12,
            run_spacing=4,
        )

        return ft.Column(
            [
                siatka,
                ft.Container(height=8),
                self._pole_cena_oferty,
                ft.Container(height=8),
                ft.ElevatedButton(
                    T.PRZYCISK_SZACUJ,
                    icon=ft.Icons.CALCULATE,
                    on_click=self._szacuj,
                    bgcolor=_KOLOR_AKCENT,
                    color="#0f172a",
                    height=48,
                ),
                ft.OutlinedButton(
                    T.PRZYCISK_OCENA_CENY,
                    icon=ft.Icons.PRICE_CHECK,
                    on_click=self._ocen_cene,
                    height=48,
                    style=ft.ButtonStyle(
                        side=ft.BorderSide(1, _KOLOR_OBRYS),
                        color=_KOLOR_TEKST,
                    ),
                ),
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

    def _buduj_widok_szacowania(self) -> ft.Control:
        """Ekran szacowania układ pionowy"""

        model_ok = self.estymator is not None

        self._panel_wynik = ft.Container(
            content=ft.Text(
                T.WYNIK_PUSTY if model_ok else T.BLAD_BRAK_MODELU,
                color=_KOLOR_TEKST_DRUGI,
                size=14,
            ),
        )
        self._panel_ocena = ft.Container(visible=False)

        naglowek = self._przycisk_powrotu("start")

        return ft.ListView(
            [
                naglowek,
                ft.Container(height=12),
                self._karta(T.SEKCJA_OPIS_NIERUCHOMOSCI, self._formularz()),
                ft.Container(height=12),
                self._karta(
                    T.SEKCJA_WYNIK,
                    ft.Column(
                        [
                            self._panel_wynik,
                            self._panel_ocena,
                        ],
                        spacing=10,
                    ),
                ),
                ft.Container(height=16),
            ],
            spacing=0,
            padding=0,
            expand=True,
        )

    def zbuduj(self) -> None:
        """Konfiguruje stronę i pokazuje ekran startowy"""

        self.page.title = T.TYTUL_APLIKACJI
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = _KOLOR_TLO
        self.page.padding = 16
        self.page.scroll = ft.ScrollMode.HIDDEN

        self._inicjalizuj_estymator()
        model_ok = self.estymator is not None
        self._loguj(
            "uruchomienie",
            f"model={'tak' if model_ok else 'nie'}",
        )

        self._kontener_widoku = ft.Column(expand=True)
        self.page.add(
            ft.SafeArea(
                expand=True,
                content=ft.Column(
                    [
                        ft.Container(content=self._kontener_widoku, expand=True),
                        ft.Container(
                            content=self._stopka(),
                            padding=ft.Padding.only(top=12),
                            alignment=ft.Alignment.BOTTOM_CENTER,
                        ),
                    ],
                    expand=True,
                    spacing=0,
                ),
            )
        )
        self._pokaz_trase("start")


def _wiersz_modelu(etykieta: str, cena: str) -> ft.Control:
    """nazwa modelu po lewej, cena po prawej"""

    return ft.Row(
        [
            ft.Text(etykieta, size=13, color=_KOLOR_TEKST_DRUGI),
            ft.Text(cena, size=15, weight=ft.FontWeight.W_600, color=_KOLOR_TEKST),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )


def _panel_wyniku_minimal(wynik) -> ft.Control:
    """blok wyników"""

    return ft.Column(
        [
            ft.Text(
                T.WYNIK_NAGLOWEK_GLOWNY,
                size=12,
                color=_KOLOR_TEKST_DRUGI,
            ),
            ft.Text(
                _formatuj_cene(wynik.random_forest.punkt),
                size=36,
                weight=ft.FontWeight.BOLD,
                color=_KOLOR_TEKST,
            ),
            ft.Text(
                T.ETYKIETA_PRZEDZIAL,
                size=12,
                color=_KOLOR_TEKST_DRUGI,
            ),
            ft.Text(
                f"{_formatuj_cene(wynik.random_forest.dol)} – {_formatuj_cene(wynik.random_forest.gora)}",
                size=15,
                weight=ft.FontWeight.W_600,
                color=_KOLOR_AKCENT,
            ),
            ft.Text(
                T.WYNIK_OPIS_PRZEDZIAL,
                size=12,
                color=_KOLOR_TEKST_DRUGI,
            ),
            ft.Container(height=12),
            ft.Divider(color=_KOLOR_OBRYS, height=1),
            ft.Container(height=8),
            _wiersz_modelu(
                T.ETYKIETA_REGRESJA_LINIOWA,
                _formatuj_cene(wynik.liniowy.punkt),
            ),
            _wiersz_modelu(
                T.ETYKIETA_RANDOM_FOREST,
                _formatuj_cene(wynik.random_forest.punkt),
            ),
        ],
        spacing=4,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )


def uruchom(page: ft.Page) -> None:
    """Punkt wejścia wywoływany z ``main.py``"""

    AplikacjaSzacowania(page).zbuduj()
