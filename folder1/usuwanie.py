import sqlite3
import pandas as pd

DB_FILE = "kv_clean.sqlite3"

conn = sqlite3.connect(DB_FILE)

# wczytaj dane
df = pd.read_sql_query("SELECT * FROM clean_ads", conn)

# kolumny bez URL
cols = [c for c in df.columns if c != "url"]

# znajdź duplikaty
duplicates = df[df.duplicated(subset=cols, keep=False)]

print(f"\nLiczba potencjalnych duplikatów: {len(duplicates)}")

if len(duplicates) > 0:
    print("\nPrzykładowe duplikaty:")
    print(duplicates.sort_values(by=cols).head(10))

    decision = input("\nCzy chcesz usunąć duplikaty? (t/n): ")

    if decision.lower() == "t":
        # zachowujemy pierwszy rekord, usuwamy resztę
        df_cleaned = df.drop_duplicates(subset=cols, keep="first")

        print(f"\nUsunięto: {len(df) - len(df_cleaned)} rekordów")

        # zapis z powrotem do bazy
        df_cleaned.to_sql("clean_ads", conn, if_exists="replace", index=False)

        print("Zaktualizowano bazę danych")

    else:
        print("Nie usunięto duplikatów")

else:
    print("Brak duplikatów")

conn.close()