import sqlite3
import pandas as pd

conn = sqlite3.connect('kv_clean.sqlite3')
df = pd.read_sql_query("SELECT * FROM clean_ads", conn)

mapowanie_stan = {
    'Uus': 'Nowy / Deweloperski',
    'Uusarendus': 'Nowy / Deweloperski',
    'Heas korras': 'Bardzo dobry',
    'Valmis': 'Bardzo dobry',
    'Renoveeritud': 'Po remoncie',
    'San. remont tehtud': 'Po remoncie',
    'Keskmine': 'Standard średni',
    'Vajab renoveerimist': 'Do remontu',
    'Vajab san. remonti': 'Do remontu'
}

mapowanie_wlasnosc = {
    'Korteriomand': 'Pełna własność',
    'Kinnistu': 'Własność (grunt)',
    'Kaasomand': 'Współwłasność',
    'Elamuühistu': 'Spółdzielcze',
    'Hoonestusõigus': 'Prawo zabudowy'
}

# Podmiana wartości w kolumnach
df['stan'] = df['stan'].str.strip().map(mapowanie_stan).fillna(df['stan'])
df['forma_wlasnosci'] = df['forma_wlasnosci'].str.strip().map(mapowanie_wlasnosc).fillna(df['forma_wlasnosci'])
df.to_sql('clean_ads', conn, if_exists='replace', index=False)

conn.close()

print("Wartości są już po polsku")