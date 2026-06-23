import sqlite3
import pandas as pd

DB_FILE = "kv_clean.sqlite3"

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# --- 1. Jakie są tabele?
print("\n📂 Tabele w bazie:")
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cur.fetchall())

# --- 2. Struktura tabeli
print("\n🧱 Struktura tabeli clean_ads:")
cur.execute("PRAGMA table_info(clean_ads);")
for col in cur.fetchall():
    print(col)

# --- 3. Ile jest rekordów
print("\n📊 Liczba rekordów:")
cur.execute("SELECT COUNT(*) FROM clean_ads;")
print(cur.fetchone()[0])

# --- 4. Podgląd pierwszych 5 rekordów
print("\n👀 Pierwsze rekordy:")
df = pd.read_sql_query("SELECT * FROM clean_ads LIMIT 5", conn)
print(df)

# --- 5. Podstawowe statystyki (ważne do regresji)
print("\n📈 Statystyki:")
df_full = pd.read_sql_query("SELECT * FROM clean_ads", conn)
print(df_full.describe())

# --- 6. Braki danych
print("\n⚠️ Braki danych (NaN):")
print(df_full.isna().sum())

conn.close()