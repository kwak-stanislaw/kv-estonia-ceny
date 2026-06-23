import sqlite3

conn = sqlite3.connect("kv_html.sqlite2")

# ile masz rekordów
count = conn.execute("SELECT COUNT(*) FROM ads").fetchone()[0]
print("Liczba rekordów:", count)

# wybierz środek
offset = count // 4

cur = conn.execute(f"""
    SELECT url, html 
    FROM ads 
    LIMIT 1 OFFSET {offset}
""")

row = cur.fetchone()

if row:
    url, html = row
    print("URL:", url)

    # zapis do pliku HTML
    with open("tess.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Zapisano do pliku tesss.html — otwórz w przeglądarce")
else:
    print("Brak danych")

conn.close()