import sqlite3
import pandas as pd

conn = sqlite3.connect('kv_clean.sqlite3')
df = pd.read_sql_query("SELECT * FROM clean_ads", conn)

mapowanie_energetyczna = {
    'puudub': 'Nieokreślona'
}

df['klasa_energetyczna'] = df['klasa_energetyczna'].str.strip().str.lower().replace(mapowanie_energetyczna)

# if_exists='replace' usunie starą tabelę i stworzy nową z polskimi danymi
df.to_sql('clean_ads', conn, if_exists='replace', index=False)

conn.close()

print("✅ Baza została zaktualizowana. Wartości są już po polsku.")