import pandas as pd
import re

def flag_words(df, column, words, new_column, case_sensitive=False):
    if isinstance(words, str):
        words = [words]  # allow a single string too

    series = df[column].astype(str)

    # Build a regex like: apple|orange|banana (escaped for safety handling special characters)
    pattern = "|".join(re.escape(w) for w in words)
    mask = series.str.contains(pattern, case=case_sensitive, na=False, regex=True)

    df = df.copy()
    df[new_column] = mask.astype(int)

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

result = flag_words(df, "comment", ["apple", "orange", "banana"], new_column="fruits")
print(result)

# How to handle pineapple?