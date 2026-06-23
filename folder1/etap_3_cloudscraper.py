import sqlite3
from bs4 import BeautifulSoup
import re

INPUT_DB = "/Users/drizzleinthebottle/Documents/1 rok ads/semestr 2/ekstrakcja danych/repozytorium/kv_html.sqlite3"
OUTPUT_DB = "kv_clean.sqlite3"

def clean_number(text):
    if not text:
        return None
    text = text.replace("\xa0", "").replace("€", "").replace(" ", "")
    text = re.sub(r"[^\d]", "", text)
    return float(text) if text else None


def extract_data(html):
    soup = BeautifulSoup(html, "html.parser")

    data = {}

    # wyciaganie ceny
    price_div = soup.find("div", class_="price-outer")
    if price_div:
        price_text = price_div.get_text(" ", strip=True)

        # cena całkowita
        price_match = re.search(r"([\d\s]+)€", price_text)
        data["cena"] = clean_number(price_match.group(1)) if price_match else None

        # cena za m2
        price_m2_match = re.search(r"([\d\s]+)€/m²", price_text)
        data["cena_za_m2"] = clean_number(price_m2_match.group(1)) if price_m2_match else None

    rows = soup.select(".meta-table tr")

    for row in rows:
        th = row.find("th")
        td = row.find("td")

        if not th or not td:
            continue

        key = th.get_text(strip=True)
        val = td.get_text(" ", strip=True)

        if "Tube" in key:
            data["liczba_pokoi"] = int(val) if val.isdigit() else None

        elif "Magamistube" in key:
            data["liczba_sypialni"] = int(val) if val.isdigit() else None

        elif "Üldpind" in key:
            data["powierzchnia_m2"] = clean_number(val)

        elif "Korrus/Korruseid" in key:
            parts = val.split("/")
            if len(parts) == 2:
                data["pietro"] = clean_number(parts[0])
                data["liczba_pieter"] = clean_number(parts[1])

        elif "Ehitusaasta" in key:
            data["rok_budowy"] = int(val) if val.isdigit() else None

        elif "Seisukord" in key:
            data["stan"] = val

        elif "Omandivorm" in key:
            data["forma_wlasnosci"] = val

        elif "Energiamärgis" in key:
            data["klasa_energetyczna"] = val

    return data


def main():
    conn_in = sqlite3.connect(INPUT_DB)
    cur_in = conn_in.cursor()

    # niepamietam w ktorej kolumnie bylo url lol
    cur_in.execute("PRAGMA table_info(ads)")
    cols = [c[1] for c in cur_in.fetchall()]
    print("Kolumny:", cols)

    html_col = "html" if "html" in cols else cols[1]

    cur_in.execute(f"SELECT url, {html_col} FROM ads")

    conn_out = sqlite3.connect(OUTPUT_DB)
    cur_out = conn_out.cursor()
    cur_out.execute("""
        CREATE TABLE IF NOT EXISTS clean_ads (
            url TEXT PRIMARY KEY,
            cena REAL,
            cena_za_m2 REAL,
            liczba_pokoi INTEGER,
            liczba_sypialni INTEGER,
            powierzchnia_m2 REAL,
            pietro INTEGER,
            liczba_pieter INTEGER,
            rok_budowy INTEGER,
            stan TEXT,
            forma_wlasnosci TEXT,
            klasa_energetyczna TEXT
        )
    """)

    count = 0

    for url, html in cur_in.fetchall():
        if not html:
            continue

        try:
            data = extract_data(html)

            cur_out.execute("""
                INSERT OR REPLACE INTO clean_ads VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                url,
                data.get("cena"),
                data.get("cena_za_m2"),
                data.get("liczba_pokoi"),
                data.get("liczba_sypialni"),
                data.get("powierzchnia_m2"),
                data.get("pietro"),
                data.get("liczba_pieter"),
                data.get("rok_budowy"),
                data.get("stan"),
                data.get("forma_wlasnosci"),
                data.get("klasa_energetyczna"),
            ))

            count += 1

        except Exception as e:
            print("Błąd:", e)

    conn_out.commit()
    conn_in.close()
    conn_out.close()

    print(f"baza gotowa ;) liczba rekordow: {count}")


if __name__ == "__main__":
    main()