"""Trening modeli regresji ceny

Architektura:

#. **Wspólny preprocessing** — imputacja braków
#. **Cel w skali log** — ``TransformedTargetRegressor`` z ``log1p``/``expm1``
#. **Dwa modele** — regresja liniowa oraz Random Forest wychwytujący nieliniowości

:author: Stanisław Kwak
:license: MIT
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

try:  # SimpleImputer ścieżka stabilna między wersjami sklearn
    from sklearn.impute import SimpleImputer
except ImportError:  # pragma: no cover
    raise

from repozytorium import __author__, __license__, __version__
from repozytorium.data import schema
from repozytorium.data.feature_engineering import BudowniczyCech
from repozytorium.data.loader import LadowarkaDanych
from repozytorium.paths import default_model_bundle_path


@dataclass
class WynikiModelu:
    """Metryki jakości pojedynczego modelu na zbiorze testowym"""

    nazwa: str
    r2: float
    mae: float
    rmse: float
    r2_cv_srednia: float
    r2_cv_odchylenie: float

    def jako_slownik(self) -> dict[str, float | str]:
        """Zwraca metryki jako słownik do raportu"""

        return {
            "nazwa": self.nazwa,
            "r2": self.r2,
            "mae": self.mae,
            "rmse": self.rmse,
            "r2_cv_srednia": self.r2_cv_srednia,
            "r2_cv_odchylenie": self.r2_cv_odchylenie,
        }


@dataclass
class PakietModeli:
    """Komplet rzeczy potrzebnych aplikacji do oceniania

    Pakiet jest eksportowany do pliku ``joblib`` i wczytywany przez
    :class:`~repozytorium.model.predykcja.Estymator`

    Attributes:
        model_liniowy: Wytrenowana regresja liniowa
        model_las: Wytrenowany Random Forest — nazwa pola zachowana dla pliku joblib
    """

    model_liniowy: Pipeline
    model_las: Pipeline
    sigma_log: dict[str, float]
    metryki: dict[str, dict]
    cechy: tuple[str, ...]
    mediana_ceny: float
    wspolczynniki_liniowe: dict[str, float] = field(default_factory=dict)
    wersja: str = __version__
    autor: str = __author__
    licencja: str = __license__
    data_treningu: str = ""


class TrenerModelu:

    def __init__(self, losowość: int = 42) -> None:
        """Ziarno generatora dla powtarzalności wyników"""

        self.losowość = losowość
        self.budowniczy = BudowniczyCech()

    def _preprocessor(self) -> ColumnTransformer:
        """imputacja skalowanie one-hot"""

        numeryczny = Pipeline(
            steps=[
                ("imputacja", SimpleImputer(strategy="median")),
                ("skalowanie", StandardScaler()),
            ]
        )
        kategoryczny = Pipeline(
            steps=[
                ("imputacja", SimpleImputer(strategy="most_frequent")),
                ("kodowanie", OneHotEncoder(handle_unknown="ignore")),
            ]
        )
        return ColumnTransformer(
            transformers=[
                ("num", numeryczny, list(schema.CECHY_NUMERYCZNE_PELNE)),
                ("kat", kategoryczny, list(schema.CECHY_KATEGORYCZNE)),
            ]
        )

    def _potok(self, regresor) -> Pipeline:
        """Składa preprocessing z regresorem uczonym na logarytmie ceny"""

        model_log = TransformedTargetRegressor(
            regressor=regresor,
            func=np.log1p,
            inverse_func=np.expm1,
        )
        return Pipeline(
            steps=[
                ("preprocessing", self._preprocessor()),
                ("model", model_log),
            ]
        )

    def _ocen(
        self,
        nazwa: str,
        potok: Pipeline,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        X: pd.DataFrame,
        y: pd.Series,
    ) -> tuple[WynikiModelu, float]:
        """Liczy metryki wskali log"""

        predykcje = potok.predict(X_test)
        r2 = float(r2_score(y_test, predykcje))
        mae = float(mean_absolute_error(y_test, predykcje))
        rmse = float(root_mean_squared_error(y_test, predykcje))

        cv = cross_val_score(potok, X, y, cv=5, scoring="r2")
        wyniki = WynikiModelu(
            nazwa=nazwa,
            r2=r2,
            mae=mae,
            rmse=rmse,
            r2_cv_srednia=float(cv.mean()),
            r2_cv_odchylenie=float(cv.std()),
        )

        reszty_log = np.log1p(y_test.to_numpy()) - np.log1p(np.maximum(predykcje, 0))
        sigma_log = float(np.std(reszty_log))
        return wyniki, sigma_log

    def _wspolczynniki_liniowe(self, potok: Pipeline) -> dict[str, float]:
        """Wyciąga współczynniki regresji liniowej wraz z nazwami cech"""

        try:
            preprocessing = potok.named_steps["preprocessing"]
            regresor = potok.named_steps["model"].regressor_
            nazwy = preprocessing.get_feature_names_out()
            wspolczynniki = regresor.coef_
            return {
                str(n): float(w) for n, w in zip(nazwy, wspolczynniki)
            }
        except Exception:  # pragma: no cover - diagnostyka pomocnicza
            return {}

    def trenuj(self, df: pd.DataFrame | None = None) -> PakietModeli:
        """Trenuje oba modele i zwraca gotowy :class:`PakietModeli`

        :param df: Dane wejściowe; gdy ``None`` — wczytywane przez
            :class:`~repozytorium.data.loader.LadowarkaDanych`
        :returns: Pakiet z modelami, metrykami i statystykami niepewności
        """

        if df is None:
            df = LadowarkaDanych().wczytaj_do_modelu()

        X, y = self.budowniczy.przygotuj_X_y(df)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=self.losowość
        )

        potok_liniowy = self._potok(LinearRegression())
        potok_las = self._potok(
            RandomForestRegressor(
                n_estimators=300,
                max_depth=None,
                min_samples_leaf=2,
                n_jobs=-1,
                random_state=self.losowość,
            )
        )

        potok_liniowy.fit(X_train, y_train)
        potok_las.fit(X_train, y_train)

        wyniki_lin, sigma_lin = self._ocen(
            "Regresja liniowa", potok_liniowy, X_test, y_test, X, y
        )
        wyniki_las, sigma_las = self._ocen(
            "Random Forest", potok_las, X_test, y_test, X, y
        )

        return PakietModeli(
            model_liniowy=potok_liniowy,
            model_las=potok_las,
            sigma_log={"liniowy": sigma_lin, "las": sigma_las},
            metryki={
                "liniowy": wyniki_lin.jako_slownik(),
                "las": wyniki_las.jako_slownik(),
            },
            cechy=schema.WSZYSTKIE_CECHY,
            mediana_ceny=float(y.median()),
            wspolczynniki_liniowe=self._wspolczynniki_liniowe(potok_liniowy),
            data_treningu=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        )

    def trenuj_i_zapisz(
        self, sciezka: str | Path | None = None
    ) -> tuple[PakietModeli, Path]:
        """Trenuje modele i zapisuje pakiet na dysk

        :param sciezka: Docelowy plik ``.joblib``; gdy ``None`` — domyślny
            z :func:`~repozytorium.paths.default_model_bundle_path`
        :returns: Pakiet modeli i ścieżka zapisu
        """

        pakiet = self.trenuj()
        cel = Path(sciezka) if sciezka else default_model_bundle_path()
        cel.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(pakiet, cel)
        return pakiet, cel


def main() -> None:
    """trenuje modele """

    trener = TrenerModelu()
    pakiet, sciezka = trener.trenuj_i_zapisz()
    print(f"Zapisano pakiet modeli: {sciezka}")
    for klucz, m in pakiet.metryki.items():
        print(
            f"[{m['nazwa']}] R2={m['r2']:.3f} "
            f"MAE={m['mae']:.0f}€ RMSE={m['rmse']:.0f}€ "
            f"R2_CV={m['r2_cv_srednia']:.3f}±{m['r2_cv_odchylenie']:.3f}"
        )


# Uruchom: PYTHONPATH=src python -c "from repozytorium.model.trening import main; main()"
# Nie używaj python -m repozytorium.model.trening — joblib zapisze klasy jako __main__
