"""Ścieżki katalogów projektu i domyślne lokalizacje baz SQL"""

from __future__ import annotations

import os
from pathlib import Path


def project_root() -> Path:
    """Zwraca katalog główny repozytorium — folder z ``kv_clean.sqlite3``

    Kolejność wykrywania:

    1. Zmienna środowiskowa ``KV_PROJECT_ROOT``
    2. Przejście w górę od pliku do folderu z ``kv_clean.sqlite3`` lub ``pyproject.toml``
    3. Domyślnie: katalog nad ``src`` w układzie developerskim
    """

    env = os.environ.get("KV_PROJECT_ROOT")
    if env:
        return Path(env).expanduser().resolve()

    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / "kv_clean.sqlite3").exists() or (parent / "pyproject.toml").exists():
            return parent

    return Path(__file__).resolve().parents[2]


def clean_ads_db_path() -> Path:
    """Ścieżka do oczyszczonej bazy ogłoszeń"""

    return project_root() / "kv_clean.sqlite3"


def artifacts_dir() -> Path:
    """Katalog na wytrenowane modele"""

    path = project_root() / "artifacts"
    path.mkdir(parents=True, exist_ok=True)
    return path


def default_model_bundle_path() -> Path:
    """Domyślny plik pakietu modeli zapisany podczas uczenia"""

    return artifacts_dir() / "model_bundle.joblib"


def app_data_dir() -> Path:
    """Katalog na lokalną bazę aplikacji"""

    path = project_root() / "data"
    path.mkdir(parents=True, exist_ok=True)
    return path


def app_database_path() -> Path:
    """Plik SQL używany logi audytu"""

    return app_data_dir() / "app.sqlite3"
