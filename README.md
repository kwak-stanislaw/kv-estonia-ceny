# KV.ee Property Price Estimator

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Author:** Stanisław Kwak · **License:** MIT

Desktop/web app that estimates Estonian real-estate prices from structured listing data and **NLP features** extracted from listing descriptions (Estonian stemming — no LLM). Built for the *Ekstrakcja i analiza danych nieustrukturyzowanych* course project.

![Stack](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Flet](https://img.shields.io/badge/GUI-Flet-14b8a6)
![sklearn](https://img.shields.io/badge/sklearn-regression-F7931E)

## Features

- **Data pipeline:** 8 978 cleaned listings from [kv.ee](https://www.kv.ee) (`kv_clean.sqlite3`)
- **NLP features:** sea proximity & city centre signals via Estonian Snowball stems
- **Models:** linear regression + random forest (log-target → always positive prices)
- **GUI (Flet):** validated form, price ranges, deal evaluation, audit logs (SQLite)
- **Partial input:** missing fields imputed like in training
- **EDA notebook:** `notebooks/eda_kv.ipynb`
- **Report (PL):** `raport/RAPORT.md`

## Quick start

```bash
# 1. Install (from repo root)
pip install -e ".[dev]"

# 2. Train models (~30 s on full dataset)
PYTHONPATH=src python scripts/trenuj_model.py

# 3. Run app
flet run src/main.py
# or web: flet run src/main.py --web

# 4. Tests
PYTHONPATH=src pytest

# 5. Code docs (HTML)
python scripts/generuj_dokumentacje.py
# → docs/html/index.html
```

## Project layout

```
src/repozytorium/   # package (data, features, model, db, ui)
folder1/            # scraping scripts (etap_1…3, usuwanie, …)
notebooks/          # EDA
raport/             # analytical report (Polish)
artifacts/          # trained model_bundle.joblib
data/               # app SQLite (audit logs)
tests/              # unit + integration tests
```

See [`PLIKI.md`](PLIKI.md) for a full file index.

## Models (test set)

| Model | R² | MAE | RMSE |
|-------|-----|-----|------|
| Linear regression | 0.62 | ~65k € | ~96k € |
| Random forest | **0.76** | ~47k € | ~77k € |

## NLP approach (course requirement)

Reference words and document tokens are reduced to **Estonian stems** (PyStemmer). Binary features `nlp_bliskosc_morza` and `nlp_centrum_miasta` fire when stem sets overlap. Inspired by course scripts `stems_lemmas.py` and `word_tag.py`.

## Submission archive

Pack **without** `.venv/` / `venv/`. Include:

- `kv_clean.sqlite3`, `artifacts/`, `src/`, `tests/`, `notebooks/`, `raport/`, `docs/html/`
- Scraping scripts in `folder1/` (no live scraping in GUI)
- [`PLIKI.md`](PLIKI.md) + [`raport/RAPORT.md`](raport/RAPORT.md)

## License

MIT — see [LICENSE](LICENSE).
