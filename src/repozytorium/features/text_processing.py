"""Lematyzacja i stemming tekstu estońskiego

Do estońskiego użyto:

- **Stanza** z ``lang='et'``
- **PyStemmer** z algorytmem Snowballa — w NLTK brak estońskiego stemmera,
  estoński jest dostępny w PyStemmer

"""

from __future__ import annotations

import re

import pandas as pd
from Stemmer import Stemmer as PyStemmerStemmer

# --- Stanza, leniwe ładowanie: pierwsze wywołanie pobiera modele --------
_stanza_nlp_et = None


def _nlp_estonski():
    """Tokenizacja i lematyzacja estońskiego"""

    global _stanza_nlp_et
    if _stanza_nlp_et is None:
        import stanza

        stanza.download("et", quiet=True)
        _stanza_nlp_et = stanza.Pipeline(
            "et",
            processors="tokenize,mwt,pos,lemma",
            verbose=False,
        )
    return _stanza_nlp_et


def _lematyzuj_tekst_estonski(tekst: str, nlp) -> str:
    if not isinstance(tekst, str) or not tekst.strip():
        return ""
    doc = nlp(tekst)
    lematy: list[str] = []
    for zdanie in doc.sentences:
        for slowo in zdanie.words:
            lemma = slowo.lemma if slowo.lemma else slowo.text
            lematy.append(lemma)
    return " ".join(lematy)


def tokenizuj_slowa(tekst: str | None) -> list[str]:
    """Tokenizacja wzorcem ``\\w+``"""

    if not isinstance(tekst, str):
        return []
    return re.findall(r"\w+", tekst, flags=re.UNICODE)


def dodaj_lematy_stanza(
    df: pd.DataFrame,
    kolumna: str,
    nowa_kolumna: str | None = None,
) -> pd.DataFrame:
    """Dodaje kolumnę z lematami Stanza dla języka estońskiego"""

    if nowa_kolumna is None:
        nowa_kolumna = f"{kolumna}_lematy_et"

    nlp = _nlp_estonski()
    df = df.copy()
    df[nowa_kolumna] = df[kolumna].apply(lambda t: _lematyzuj_tekst_estonski(t, nlp))
    return df


_stemmer_et = PyStemmerStemmer("estonian")


def dodaj_korzenie_estonskie(
    df: pd.DataFrame,
    kolumna: str,
    nowa_kolumna: str | None = None,
) -> pd.DataFrame:
    """Dodaje kolumnę ze słowami po stemmingu"""

    if nowa_kolumna is None:
        nowa_kolumna = f"{kolumna}_korzenie_et"

    def korzenie(wiersz: object) -> str:
        if not isinstance(wiersz, str):
            return ""
        tokeny = tokenizuj_slowa(wiersz)
        if not tokeny:
            return ""
        return " ".join(_stemmer_et.stemWords(tokeny))

    df = df.copy()
    df[nowa_kolumna] = df[kolumna].apply(korzenie)
    return df


def dodaj_lematy_spacy(
    df: pd.DataFrame,
    kolumna: str,
    model_spacy: str,
    nowa_kolumna: str | None = None,
    zachowaj_interpunkcje: bool = False,
):
    """Lematy spaCy — podaj nazwę zainstalowanego modelu

    Wcześniej: ``python -m spacy download en_core_web_sm``
    """

    import spacy

    if nowa_kolumna is None:
        nowa_kolumna = f"{kolumna}_lematy_spacy"

    nlp = spacy.load(model_spacy)

    def lematyzuj(tekst: object) -> str:
        if not isinstance(tekst, str):
            return ""
        dokument = nlp(tekst)
        if zachowaj_interpunkcje:
            tokeny = [t.lemma_ for t in dokument]
        else:
            tokeny = [
                t.lemma_
                for t in dokument
                if not t.is_punct and not t.is_space
            ]
        return " ".join(tokeny)

    df = df.copy()
    df[nowa_kolumna] = df[kolumna].apply(lematyzuj)
    return df


def dodaj_korzenie_porter(
    df: pd.DataFrame,
    kolumna: str,
    nowa_kolumna: str | None = None,
):
    """Stemmer Portera"""

    import nltk
    from nltk.stem import PorterStemmer
    from nltk.tokenize import word_tokenize

    nltk.download("punkt_tab", quiet=True)

    if nowa_kolumna is None:
        nowa_kolumna = f"{kolumna}_porter"

    stemmer = PorterStemmer()

    def korzenie(tekst: object) -> str:
        if not isinstance(tekst, str):
            return ""
        tokeny = word_tokenize(tekst)
        return " ".join(stemmer.stem(t) for t in tokeny)

    df = df.copy()
    df[nowa_kolumna] = df[kolumna].apply(korzenie)
    return df


def dodaj_korzenie_snowball(
    df: pd.DataFrame,
    kolumna: str,
    jezyk: str = "english",
    nowa_kolumna: str | None = None,
):
    """Stemmer Snowball"""

    import nltk
    from nltk.stem import SnowballStemmer
    from nltk.tokenize import word_tokenize

    nltk.download("punkt_tab", quiet=True)

    if nowa_kolumna is None:
        nowa_kolumna = f"{kolumna}_snowball_{jezyk}"

    stemmer = SnowballStemmer(jezyk)

    def korzenie(tekst: object) -> str:
        if not isinstance(tekst, str):
            return ""
        tokeny = word_tokenize(tekst)
        return " ".join(stemmer.stem(t) for t in tokeny)

    df = df.copy()
    df[nowa_kolumna] = df[kolumna].apply(korzenie)
    return df


# Aliasy angielskie
add_spacy_lemmas = dodaj_lematy_spacy
add_porter_stems = dodaj_korzenie_porter
add_snowball_stems = dodaj_korzenie_snowball
