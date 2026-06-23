import sqlite3
import os
import re
import requests
import time
from pathlib import Path

HTML_DB = "/Users/drizzleinthebottle/Documents/1 rok ads/semestr 2/ekstrakcja danych/repozytorium/kv_html.sqlite3"
CLEAN_DB = "/Users/drizzleinthebottle/Documents/1 rok ads/semestr 2/ekstrakcja danych/repozytorium/kv_clean.sqlite3"
OUTPUT_DIR = "/Users/drizzleinthebottle/Documents/1 rok ads/semestr 2/ekstrakcja danych/repozytorium/folder1/zdjecia"
SLEEP_TIME = 0.3  

os.makedirs(OUTPUT_DIR, exist_ok=True)


def get_clean_urls():
    conn = sqlite3.connect(CLEAN_DB)
    cur = conn.cursor()

    cur.execute("SELECT url FROM clean_ads")
    urls = {row[0] for row in cur.fetchall()}

    conn.close()
    print(f"Loaded {len(urls)} URLs from clean_ads")
    return urls


def extract_img_url(html):
    """Wyciąga główne zdjęcie (swiper active)."""
    match = re.search(
        r'swiper-slide-active.*?<img[^>]+src="([^"]+)"',
        html,
        re.DOTALL
    )

    if not match:
        return None

    url = match.group(1)

    # filtr
    if not url.startswith("http"):
        return None
    if ".svg" in url:
        return None

    return url


def download_image(url, filename):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
        "Referer": "https://www.kv.ee/"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()

        with open(filename, "wb") as f:
            f.write(r.content)

        return True

    except Exception as e:
        print(f"Failed: {url} → {e}")
        return False


def main():
    clean_urls = get_clean_urls()

    conn = sqlite3.connect(HTML_DB)
    cur = conn.cursor()

    cur.execute("SELECT url, html FROM ads")

    processed = 0
    saved = 0

    for url, html in cur.fetchall():
        if url not in clean_urls:
            continue

        img_url = extract_img_url(html)

        if not img_url:
            continue

        filename = os.path.join(OUTPUT_DIR, f"{saved}.jpg")

        if download_image(img_url, filename):
            saved += 1

        processed += 1

        # sleep żeby nie dostać bana
        time.sleep(SLEEP_TIME)

        if processed % 50 == 0:
            print(f"Processed: {processed}, saved: {saved}")

    conn.close()

    print(f"\nDONE → saved {saved} images")


if __name__ == "__main__":
    main()