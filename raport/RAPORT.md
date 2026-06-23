# Raport analityczny — projekt zaliczeniowy

**Autor:** Stanisław Kwak  
**Licencja:** MIT  
**Źródło danych:** [kv.ee](https://www.kv.ee) — estońskie ogłoszenia sprzedaży nieruchomości

---

## 1. Proces zbierania danych

| Etap | Opis | Wynik |
|------|------|-------|
| 1 | Pobranie linków (`etap_1_cloudscraper.py`, cloudscraper) | **9 512** URL-i z 191 stron listingu |
| 2 | Pobranie HTML (Playwright, `etap_2_cloudscraper.py`) | baza `kv_html.sqlite3` |
| 3 | Parsowanie i czyszczenie (`etap_3_cloudscraper.py`) | tabela `clean_ads` |
| 4 | Usunięcie rekordów bez ceny | −159 → **9 353** |
| 5 | Usunięcie duplikatów (`usuwanie.py`) | −180 → **9 173** |
| 6 | Filtr cen 10 000–2 000 000 € | −194 → **8 979** |
| 7 | Uzupełnienie opisu i danych sprzedawcy | kolumny `opis`, `sprzedawca_*` |

**Stan końcowy w aplikacji:** **8 978** ogłoszeń z ceną w sensownym zakresie (po dodatkowym filtrze loadera).

Numer telefonu nie został wyekstrahowany — wartość ładowana jest dynamicznie po kliknięciu w przeglądarce (brak w statycznym HTML).

---

## 2. Eksploracyjna analiza danych (EDA)

Szczegółowe wykresy i tabele: notebook [`notebooks/eda_kv.ipynb`](notebooks/eda_kv.ipynb).

**Statystyki opisowe (wybrane):**

- **Cena:** mediana ≈ **159 900 €**, min 10 000 €, max 1 700 000 €
- **Powierzchnia:** typowo 30–120 m² (rozkład prawoskośny)
- **Stan:** dominują „Nowy / Deweloperski” i „Bardzo dobry”
- **Forma własności:** głównie „Pełna własność” (~81%)
- **Opis:** brak tekstu w ~145 rekordach (imputacja w modelu)

**Obserwacje:**

1. Rozkład ceny jest silnie skośny — stąd transformacja logarytmiczna celu w modelu.
2. Powierzchnia i liczba pokoi korelują dodatnio z ceną.
3. Ogłoszenia z sygnałem **bliskości morza** (~28%) i **centrum miasta** (~39%) w opisie występują często — sensowne predyktory lokalizacyjne.

---

## 3. Transformacje i inżynieria cech

### 3.1 Cechy strukturalne (z HTML)

Numeryczne: `powierzchnia_m2`, `liczba_pokoi`, `liczba_sypialni`, `pietro`, `liczba_pieter`, `rok_budowy`.  
Kategoryczne (one-hot w potoku): `stan`, `forma_wlasnosci`, `klasa_energetyczna`.

Wartości estońskie przetłumaczono na polskie kategorie semantyczne (słownik mapowań w etapie czyszczenia).

### 3.2 Cechy tekstowe (NLP — **bez LLM**)

Metoda zgodna z wymaganiami projektu i materiałami z zajęć (`stems_lemmas`, `word_tag`):

1. **Tokenizacja** (`\w+`, Unicode).
2. **Stemming Snowball dla estońskiego** (PyStemmer) — ten sam algorytm dla słów referencyjnych i dokumentu.
3. **Dopasowanie na zbiorach korzeni** — binarne cechy:
   - `nlp_bliskosc_morza` — m.in. *meri, rand, rannik, promenaad*
   - `nlp_centrum_miasta` — m.in. *kesklinn, vanalinn, keskus*
4. **Statystyki opisu:** `dlugosc_opisu_znaki`, `liczba_slow_opisu`.

Implementacja: `src/repozytorium/features/cechy_lokalizacji_nlp.py`.

Opcjonalnie dostępna lematyzacja Stanza (`lang='et'`) w `text_processing.py` — do analiz eksploracyjnych; w produkcyjnym potoku używamy stemmera (szybszy, bez pobierania dużych modeli).

### 3.3 Preprocessing modelu

- Imputacja medianą (numeryczne) / modą (kategoryczne)
- Standaryzacja cech numerycznych
- One-hot encoding kategorii (`handle_unknown='ignore'`)
- Cel: `log1p(cena)` → predykcje zawsze dodatnie (`expm1` odwrotna)

---

## 4. Historia budowy modelu i diagnostyka

**Podział:** 80% trening / 20% test, `random_state=42`, walidacja krzyżowa 5-fold (R²).

| Model | R² (test) | MAE | RMSE | R² CV (średnia ± sd) |
|-------|-----------|-----|------|----------------------|
| Regresja liniowa | **0,621** | 64 856 € | 96 042 € | niestabilna (duża wariancja CV) |
| Random Forest | **0,759** | 46 845 € | 76 626 € | **0,705 ± 0,040** |

**Diagnostyka:**

- Random Forest lepiej wychwytuje nieliniowości (interakcje powierzchnia × lokalizacja).
- Regresja liniowa służy jako model interpretowalny (współczynniki w pakiecie `model_bundle.joblib`).
- Reszty w skali log służą do **widełek cenowych** (~80% przedział predykcyjny w aplikacji).
- Świadomie **pominięto** `cena_za_m2` w predyktorach (data leakage).

Trening: `python scripts/trenuj_model.py` → `artifacts/model_bundle.joblib`.

---

## 5. Model w aplikacji

Aplikacja Flet (`src/main.py`) korzysta z **obu modeli**:

- wyświetla oszacowanie punktowe i przedział dla regresji liniowej i lasu,
- uśrednia oba modele jako podpowiedź,
- ocenia podaną cenę oferty (korzystna / przeciętna / za wysoka) względem przedziału lasu,
- pozwala na **niepełne dane wejściowe** (imputacja jak w treningu),
- zapisuje **logi audytu** w SQLite (`data/app.sqlite3`) — dostęp z małej ikonki w stopce.

---

## 6. Opis popularno-naukowy

Program zbierał ogłoszenia z estońskiego portalu nieruchomości, a następnie „uczył się”, jak cena zależy od metrażu, liczby pokoi, stanu mieszkania oraz od tego, co napisano w opisie — np. czy wspomniano o morzu albo centrum miasta. Do rozpoznawania takich wzmianek nie użyto sztucznej inteligencji w sensie LLM, lecz klasyczne narzędzia językoznawcze: dzielenie tekstu na słowa i sprowadzanie ich do wspólnych korzeni.

Na tej podstawie zbudowano dwa modele statystyczne. Prostszy (regresja liniowa) pokazuje ogólne zależności; dokładniejszy (Random Forest) lepiej trafia w konkretne ceny. Aplikacja na telefonie lub komputerze pozwala wpisać parametry mieszkania i otrzymać szacunek w euro wraz z widełkami — a także sprawdzić, czy cena w ogłoszeniu wydaje się atrakcyjna.

---

## 7. Uruchomienie

```bash
pip install -e ".[dev]"
python scripts/trenuj_model.py
flet run src/main.py
pytest
python scripts/generuj_dokumentacje.py
```

Dokumentacja kodu: `docs/html/index.html`.
