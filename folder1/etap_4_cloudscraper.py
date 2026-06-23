import sqlite3

DB_FILE = "kv_clean.sqlite3"

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# sprawdź ile rekordów przed
cur.execute("SELECT COUNT(*) FROM clean_ads")
before = cur.fetchone()[0]

# usuń rekordy bez ceny
cur.execute("DELETE FROM clean_ads WHERE price IS NULL")

conn.commit()

# sprawdź ile po
cur.execute("SELECT COUNT(*) FROM clean_ads")
after = cur.fetchone()[0]

conn.close()

print(f"Przed: {before}")
print(f"Po: {after}")
print(f"Usunięto: {before - after}")