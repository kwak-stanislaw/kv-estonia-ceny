from playwright.sync_api import sync_playwright
import sqlite3
import time
import random

DB_FILE = "kv_html.sqlite3"
INPUT_FILE = "/Users/drizzleinthebottle/Documents/1 rok ads/semestr 2/ekstrakcja danych/repozytorium/folder1/ogloszenia.txt"

def main():
    conn = sqlite3.connect(DB_FILE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS ads (
            url TEXT PRIMARY KEY,
            html TEXT
        )
    """)

    with open(INPUT_FILE, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        context = browser.new_context()
        page = context.new_page()

        # wejscie na strone glowną
        page.goto("https://www.kv.ee/")

        print("\njesli sie pojawi, rozwiąż Cloudflare ręcznie, potem wcisnij enter\n")
        input()

        success = 0

        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}] {url}")

            for attempt in range(3):  # retry
                try:
                    page.goto(url, timeout=60000)

                    # symulowanie ludzkiej aktywności
                    page.mouse.move(random.randint(100, 800), random.randint(100, 600))
                    page.wait_for_timeout(random.randint(500, 1500))

                    html = page.content()

                    # sprawdzenie blokady narzuconej przez cloudlfare
                    if "Just a moment" in html:
                        print("Cloudflare blokada — retry")
                        time.sleep(random.uniform(5, 10))
                        continue

                    # zapisanie wynikow w bazie sql
                    conn.execute(
                        "INSERT OR REPLACE INTO ads (url, html) VALUES (?, ?)",
                        (url, html)
                    )
                    conn.commit()

                    success += 1
                    print(f"gotowe (zebrane: {success})")
                    break

                except Exception as e:
                    print(f"błąd {e}")
                    time.sleep(5)

            # zastosowanie opoznienia
            time.sleep(random.uniform(4, 8))

            # restart sesji co 30 stron
            if i % 30 == 0:
                print("Restart sesji przegladarki")
                context.close()
                context = browser.new_context()
                page = context.new_page()
                page.goto("https://www.kv.ee/")
                time.sleep(5)

        browser.close()

    conn.close()

    print(f"\nPoprawnie zapisano: {success}")

if __name__ == "__main__":
    main()