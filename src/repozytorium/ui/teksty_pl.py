"""Stałe tekstowe interfejsu użytkownika"""

TYTUL_APLIKACJI = "Szacowanie cen estońskich nieruchomości"
PODTYTUL_ZRODLO = "Dane: kv.ee"
PODTYTUL_MODELE = "Modele: regresja liniowa oraz Random Forest"

# Strona startowa
START_OPIS_KROTKI = (
    "Aplikacja szacuje cenę mieszkania na podstawie parametrów ogłoszenia "
    "Podaj co najmniej jeden parametr, a brakujące wartości uzupełni model. "
)
PRZYCISK_DO_SZACOWANIA = "Rozpocznij"
PRZYCISK_O_APLIKACJI = "O aplikacji"
PRZYCISK_POWROT = "Wróć"

# O aplikacji
TYTUL_O_APLIKACJI = "O aplikacji"
O_APLIKACJI_WSTEP = (
    "Program korzysta z danych ogłoszeń z estońskiej strony kv.ee "
    "Na ich podstawie wytrenowano dwa modele statystyczne, które przewidują "
    "cenę sprzedaży nieruchomości w euro."
)
O_APLIKACJI_REGRESJA = (
    "**Regresja liniowa** zakłada, że cena zmienia się w sposób liniowy "
    "względem cech (np. większy metraż → wyższa cena). Model w tej aplikacji uczy się "
    "współczynników na tysiącach ogłoszeń ze strony kv.ee metodą najmniejszych "
    "kwadratów. Jest szybki i łatwy do interpretacji, ale nie wychwytuje "
    "skomplikowanych zależności."
)
O_APLIKACJI_RF = (
    "**Random Forest.** Ceny nieruchomości zależą od skomplikowanych kwestii. "
    "Regresja liniowa może nie odwzorowywać wszystkich zależności. "
    "Dlatego zastosowano algorytm Random Forest, który tworzy "
    "wiele drzew decyzyjnych, analizujących różne kombinacje cech nieruchomości. "
    "Końcowa prognoza ceny jest średnią wyników uzyskanych przez wszystkie drzewa."
)
O_APLIKACJI_WYNIK = (
    "Aplikacja pokazuje oszacowanie z obu modeli oraz **przedział cenowy**. "
    "Możesz też podać cenę z ogłoszenia — program oceni, czy wygląda "
    "na korzystną, typową czy zawyżoną względem przewidywanego przedziału. "
    "Ceny są liczone w skali logarytmicznej, aby uniknąć nierealistycznych "
    "wartości ujemnych."
)

# Sekcje
SEKCJA_OPIS_NIERUCHOMOSCI = "Parametry nieruchomości"
SEKCJA_LOKALIZACJA = "Cechy z opisu ogłoszenia"
ETYKIETA_DOSTEP_MORZE = "Dostęp do morza"
ETYKIETA_CENTRUM = "Centrum miasta w pobliżu"
OPCJA_TAK = "Tak"
OPCJA_NIE = "Nie"
SEKCJA_WYNIK = "Wynik"
SEKCJA_OCENA_OFERTY = "Ocena ceny"
WYNIK_NAGLOWEK_GLOWNY = "Szacowana cena (Random Forest)"
WYNIK_PUSTY = "Uzupełnij parametry i kliknij „Szacuj cenę”."

# Pola formularza
ETYKIETA_POWIERZCHNIA = "Powierzchnia (m²)"
ETYKIETA_POKOI = "Liczba pokoi"
ETYKIETA_SYPIALNI = "Liczba sypialni"
ETYKIETA_PIETRO = "Piętro"
ETYKIETA_ROK_BUDOWY = "Rok budowy"
ETYKIETA_STAN = "Stan"
ETYKIETA_KLASA_ENERGETYCZNA = "Klasa energetyczna"
ETYKIETA_FRAGMENT_OPISU = ""  # nieużywane — NLP tylko w ETL
ETYKIETA_CENA_OFERTY = "Cena z ogłoszenia (€, opcjonalnie)"

PODPOWIEDZ_POWIERZCHNIA = "np. 52,5"
PODPOWIEDZ_LICZBA = "tylko cyfry"
PODPOWIEDZ_OPCJONALNE = "opcjonalnie"

# Przyciski
PRZYCISK_SZACUJ = "Szacuj cenę"
PRZYCISK_OCENA_CENY = "Oceń podaną cenę"
PRZYCISK_ZAMKNIJ = "Zamknij"
PRZYCISK_WYCZYSC_LOGI = "Wyczyść logi"

# Logi audytu (ukryte w stopce — mała ikonka)
LOGI_AUDYTU_TOOLTIP = "Logi audytu (administracja)"
TYTUL_LOGI_AUDYTU = "Logi audytu"
LOGI_PUSTE = "Brak zapisanych zdarzeń."
LOGI_WYCZYSZCZONO = "Wyczyszczono logi audytu."

# Komunikaty
BLAD_BRAK_MODELU = (
    "Brak wytrenowanego modelu. Uruchom najpierw skrypt uczenia "
    "(np. python scripts/trenuj_model.py)."
)
BLAD_WARTOSC_LICZBOWA = "Podaj poprawną liczbę (np. 48 lub 48,5)."
BLAD_ZAKRES = "Wartość poza ustalonym zakresem."
SUKCES_OBLICZENIO = "Oszacowanie gotowe."

# Wynik
ETYKIETA_REGRESJA_LINIOWA = "Regresja liniowa"
ETYKIETA_RANDOM_FOREST = "Random Forest"
ETYKIETA_PRZEDZIAL = "Typowy zakres cen: "
WYNIK_OPIS_PRZEDZIAL = (
    "Model na danych treningowych zwykle myli się o pewną kwotę. "
    "Ten zakres obejmuje ok. 80% takich przypadków — u większości "
    "podobnych ogłoszeń cena mieściłaby się między dolną a górną granicą."
)
OCENA_TEKST_KORZYSTNA = "Cena wygląda na korzystną :) Jest poniżej dolnej granicy przedziału"
OCENA_TEKST_PRZECIETNA = "Cena w typowym przedziale"
OCENA_TEKST_WYSOKA = "Cena jest zbyt wysoka — powyżej górnej granicy przedziału"
BLAD_BRAK_PARAMETROW = (
    "Podaj co najmniej jeden parametr nieruchomości "
    "(np. powierzchnię, liczbę pokoi lub rok budowy)."
)
BLAD_POKOI_SYPIALNIE = (
    "Liczba pokoi musi być większa niż liczba sypialni."
)
ETYKIETA_SREDNIA_MODELI = "Średnia obu modeli"
