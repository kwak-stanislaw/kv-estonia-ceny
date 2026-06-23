import pandas as pd
import spacy
import nltk
from nltk.stem import PorterStemmer, SnowballStemmer
from nltk.tokenize import word_tokenize

# One-time downloads for NLTK (safe to call repeatedly)
nltk.download("punkt_tab", quiet=True)

# Load spaCy model once at module level (loading is slow)
# Run in terminal first: python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")
# Basic models:
# en_core_web_sm — small (~12 MB), fast, no word vectors basic tokenization, POS, NER, parsing.
# en_core_web_md — medium (~40 MB), 300d word vectors better accuracy, supports similarity.
# en_core_web_lg — large (~560 MB), full word vectors highest accuracy of CPU pipelines.
# en_core_web_trf — transformer-based (RoBERTa, ~440 MB) state-of-the-art accuracy, slow on CPU,
# For polish:
# pl_core_news_sm, pl_core_news_md, pl_core_news_lg
# No official pl_core_news_trf, adequate model must be downloaded from hf

def add_spacy_lemmas(df, column, new_column=None, keep_punct=False):
    """
    Add a column with spaCy lemmas of the text.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        column (str): Column with text to process.
        new_column (str): Name for output column. Defaults to f"{column}_lemmas".
        keep_punct (bool): If False, drops punctuation and spaces.
    """
    if new_column is None:
        new_column = f"{column}_lemmas"

    def lemmatize(text):
        if not isinstance(text, str):
            return ""
        doc = nlp(text) # tokenization is done here
        if keep_punct:
            tokens = [token.lemma_ for token in doc]
        else:
            tokens = [token.lemma_ for token in doc if not token.is_punct and not token.is_space]
        return " ".join(tokens)

    df = df.copy()
    df[new_column] = df[column].apply(lemmatize)
    return df


def add_porter_stems(df, column, new_column=None):
    """
    Add a column with NLTK Porter stems of the text.
    Porter is the classic English stemmer — aggressive and fast.
    """
    if new_column is None:
        new_column = f"{column}_porter"

    stemmer = PorterStemmer()

    def stem(text):
        if not isinstance(text, str):
            return ""
        tokens = word_tokenize(text)
        return " ".join(stemmer.stem(t) for t in tokens)

    df = df.copy()
    df[new_column] = df[column].apply(stem)
    return df


def add_snowball_stems(df, column, new_column=None, language="english"):
    """
    Add a column with NLTK Snowball stems.
    """
    if new_column is None:
        new_column = f"{column}_snowball"

    stemmer = SnowballStemmer(language)

    def stem(text):
        if not isinstance(text, str):
            return ""
        tokens = word_tokenize(text)
        return " ".join(stemmer.stem(t) for t in tokens)

    df = df.copy()
    df[new_column] = df[column].apply(stem)
    return df

data = {
    "comment": [
        "I love apples and oranges",
        "I love bananas",
        "I love pineapples",
        "I love bananas",
        "bananas are great",
        "ORANGE juice please",
        "no fruit here",
        None,
    ]
}
df = pd.DataFrame(data)
df = add_spacy_lemmas(df, "comment")
df = add_porter_stems(df, "comment")
df = add_snowball_stems(df, "comment")
print(df.head().to_string())
