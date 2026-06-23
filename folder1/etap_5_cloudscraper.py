import sqlite3
import re
from bs4 import BeautifulSoup

INPUT_DB = "/Users/drizzleinthebottle/Documents/1 rok ads/semestr 2/ekstrakcja danych/repozytorium/kv_html.sqlite3"
OUTPUT_DB = "/Users/drizzleinthebottle/Documents/1 rok ads/semestr 2/ekstrakcja danych/repozytorium/kv_clean.sqlite3"

def add_column_if_missing(cur, table_name, column_name, column_type):
    cur.execute(f"PRAGMA table_info({table_name})")
    existing_columns = [row[1] for row in cur.fetchall()]
    if column_name not in existing_columns:
        cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")

def clean_text(text):
    if text is None:
        return None
    text = text.replace("\xa0", " ")
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines) if lines else None

def extract_description(soup):
    desc = soup.select_one("p.description-content")
    if not desc:
        return None
    return clean_text(desc.get_text("\n"))

def split_name(full_name):
    if not full_name:
        return None, None
    parts = full_name.split()
    if len(parts) == 1:
        return parts[0], None
    return parts[0], " ".join(parts[1:])

def extract_broker_data(soup):
    broker = soup.select_one(".broker")
    if not broker:
        return None, None, None, None

    name_el = broker.select_one("a.name")
    company_el = broker.select_one('a[href^="/firma/"]')
    phone_el = soup.select_one('.broker-contacts a[href^="tel:"]')

    full_name = name_el.get_text(" ", strip=True) if name_el else None
    imie, nazwisko = split_name(full_name)

    firma = company_el.get_text(" ", strip=True) if company_el else None

    telefon = None
    if phone_el and phone_el.get("href"):
        tel_href = phone_el.get("href")
        phone_match = re.sub(r"\D", "", tel_href)
        telefon = phone_match if phone_match else phone_el.get_text(" ", strip=True)

    return imie, nazwisko, firma, telefon

def main():
    conn_in = sqlite3.connect(INPUT_DB)
    cur_in = conn_in.cursor()

    conn_out = sqlite3.connect(OUTPUT_DB)
    cur_out = conn_out.cursor()

    # dodaj brakujące kolumny do istniejącej tabeli clean_ads
    add_column_if_missing(cur_out, "clean_ads", "opis", "TEXT")
    add_column_if_missing(cur_out, "clean_ads", "sprzedawca_imie", "TEXT")
    add_column_if_missing(cur_out, "clean_ads", "sprzedawca_nazwisko", "TEXT")
    add_column_if_missing(cur_out, "clean_ads", "sprzedawca_firma", "TEXT")
    add_column_if_missing(cur_out, "clean_ads", "numer_telefonu", "TEXT")

    # sprawdź kolumny w ads i znajdź kolumnę html
    cur_in.execute("PRAGMA table_info(ads)")
    cols = [row[1] for row in cur_in.fetchall()]
    if "html" in cols:
        html_col = "html"
    else:
        html_col = cols[1]  # awaryjnie

    # pobierz tylko URL-e, które istnieją w clean_ads
    cur_out.execute("SELECT url FROM clean_ads")
    urls_in_clean = {row[0] for row in cur_out.fetchall()}

    # czytamy html z tabeli ads
    cur_in.execute(f"SELECT url, {html_col} FROM ads")

    updated = 0
    skipped = 0

    for url, html in cur_in.fetchall():
        if url not in urls_in_clean:
            skipped += 1
            continue

        if not html:
            skipped += 1
            continue

        try:
            soup = BeautifulSoup(html, "html.parser")

            opis = extract_description(soup)
            imie, nazwisko, firma, telefon = extract_broker_data(soup)

            cur_out.execute("""
                UPDATE clean_ads
                SET opis = ?,
                    sprzedawca_imie = ?,
                    sprzedawca_nazwisko = ?,
                    sprzedawca_firma = ?,
                    numer_telefonu = ?
                WHERE url = ?
            """, (opis, imie, nazwisko, firma, telefon, url))

            updated += 1

        except Exception as e:
            print(f"Błąd przy URL {url}: {e}")

    conn_out.commit()
    conn_in.close()
    conn_out.close()

    print(f"Gotowe. Uzupełniono: {updated}")
    print(f"Pominięto: {skipped}")

if __name__ == "__main__":
    main()