# Opis plików projektu

**Autor:** Stanisław Kwak · **Licencja:** MIT

## Katalog główny

| Plik / folder | Opis |
|---------------|------|
| `kv_clean.sqlite3` | Oczyszczona baza ogłoszeń (tabela `clean_ads`) — **dołączyć do archiwum zaliczeniowego** |
| `kv_html.sqlite3` | Surowe HTML ogłoszeń (duży plik — opcjonalnie w archiwum) |
| `artifacts/model_bundle.joblib` | Wytrenowane modele regresji + metryki |
| `data/app.sqlite3` | Logi audytu (tworzone przy pierwszym uruchomieniu GUI) |
| `pyproject.toml` | Zależności i konfiguracja projektu |
| `LICENSE` | Licencja MIT |
| `README.md` | Instrukcja uruchomienia (GitHub) |

## Kod źródłowy (`src/`)

| Ścieżka | Opis |
|---------|------|
| `src/main.py` | Punkt wejścia aplikacji Flet |
| `src/repozytorium/data/loader.py` | Wczytywanie danych z SQLite |
| `src/repozytorium/data/schema.py` | Nazwy kolumn i stałe projektu |
| `src/repozytorium/data/feature_engineering.py` | Budowa macierzy cech |
| `src/repozytorium/features/text_processing.py` | Lematy (Stanza) i stemmy (PyStemmer, NLTK) |
| `src/repozytorium/features/cechy_lokalizacji_nlp.py` | Cechy morze/centrum przez stemming ET |
| `src/repozytorium/features/text_keywords.py` | Agregacja cech tekstowych |
| `src/repozytorium/model/trening.py` | Trening regresji liniowej i Random Forest |
| `src/repozytorium/model/predykcja.py` | Oszacowania, przedziały, ocena oferty |
| `src/repozytorium/db/logi_audytu.py` | SQLite: logi audytu użycia GUI |
| `src/repozytorium/ui/aplikacja.py` | GUI Flet |
| `src/repozytorium/ui/walidacja.py` | Walidacja pól formularza |
| `src/repozytorium/ui/teksty_pl.py` | Teksty interfejsu po polsku |

## Skrypty scrapingu (`folder1/`)

| Plik | Opis |
|------|------|
| `etap_1_cloudscraper.py` | Pobieranie linków ogłoszeń |
| `etap_2_cloudscraper.py` | Pobieranie HTML (Playwright) |
| `etap_3_cloudscraper.py` | Parsowanie do `clean_ads` |
| `usuwanie.py` | Usuwanie duplikatów |
| `eksporter_zdjec.py` | Pobieranie zdjęć ogłoszeń |
| `ogloszenia.txt` | Lista URL-i (9512 linków) |

## Analiza i dokumentacja

| Plik | Opis |
|------|------|
| `notebooks/eda_kv.ipynb` | EDA — rozkłady, korelacje, cechy NLP |
| `raport/RAPORT.md` | Raport analityczny (PL) |
| `docs/html/` | Dokumentacja kodu (HTML, pdoc) |
| `scripts/generuj_dokumentacje.py` | Generator dokumentacji |
| `tests/` | Testy jednostkowe i integracyjne |

## Testy

| Plik | Zakres |
|------|--------|
| `tests/test_cechy_nlp.py` | Stemming i cechy lokalizacji |
| `tests/test_walidacja.py` | Walidacja GUI |
| `tests/test_logi_audytu.py` | Logi audytu |
| `tests/test_integracja_model.py` | Trening + predykcja (integracja) |

## Czego **nie** wrzucać na GitHub / do zip

- `.venv/`, `venv/` — wirtualne środowisko
- `kv_html.sqlite3` — można pominąć ze względu na rozmiar (~6 GB) i compliance
- Surowe zdjęcia — opcjonalnie w osobnym folderze lokalnie
