# prosty_scraper_kv.py
import os
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# ====== KONFIG ======
TOTAL_LISTINGS = 24290       # podałeś, że jest 24 290 ogłoszeń
STEP = 50                    # start=0,50,100,...
BASE_SEARCH = "https://www.kv.ee/search"
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 '
                  '(KHTML, like Gecko) Version/26.2 Safari/605.1.15',
    'Accept-Language': 'pl-PL,pl;q=0.9',
}
OUT_DIR = "kv_pages"
PAGES_DIR = os.path.join(OUT_DIR, "pages")
LISTINGS_OUT = os.path.join(OUT_DIR, "listing_urls.txt")

# jeśli masz legalne proxy, wpisz tu: {"http": "...", "https": "..."} lub zostaw None
PROXIES = None

# ====== UTILS ======
os.makedirs(PAGES_DIR, exist_ok=True)
session = requests.Session()
session.headers.update(HEADERS)

def safe_sleep(min_s=0.6, max_s=1.2):
    time.sleep(min_s + random.random() * (max_s - min_s))

def save_file(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

# ====== 1) PĘTLA PO STRONACH WYNIKÓW ======
def fetch_search_pages(total=TOTAL_LISTINGS, step=STEP):
    last_start = ((total - 1) // step) * step  # np. dla 24290 -> 24250
    starts = list(range(0, last_start + 1, step))
    print(f"Pobiorę {len(starts)} stron (start od {starts[0]} do {starts[-1]} co {step})")
    for start in starts:
        url = f"{BASE_SEARCH}?start={start}"
        fname = os.path.join(PAGES_DIR, f"search_start_{start}.html")
        # jeśli już pobrane, możesz pominąć (przy resume)
        if os.path.exists(fname):
            print(f"-> {fname} już istnieje — pomijam")
            continue
        tries = 0
        while tries < 3:
            try:
                print(f"Pobieram {url} ...", end="")
                r = session.get(url, proxies=PROXIES, timeout=20)
                print(f" status {r.status_code}")
                if r.status_code == 200:
                    save_file(fname, r.text)
                    safe_sleep()
                    break
                else:
                    tries += 1
                    print("Nie 200, retry... (status:", r.status_code, ")")
                    time.sleep(2)
            except Exception as e:
                tries += 1
                print("Błąd:", e, " - retry")
                time.sleep(2)
        else:
            print(f"Nie udało się pobrać {url} po 3 próbach. Przechodzę dalej.")

# ====== 2) EKSTRAKCJA LINKÓW DO OGŁOSZEŃ Z ZAPISANYCH STRON ======
def extract_listing_urls():
    urls = set()
    files = sorted(f for f in os.listdir(PAGES_DIR) if f.endswith(".html"))
    for f in files:
        path = os.path.join(PAGES_DIR, f)
        with open(path, "r", encoding="utf-8") as fh:
            html = fh.read()
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            # normalizacja
            if href.startswith("//"):
                href = "https:" + href
            elif href.startswith("/"):
                href = urljoin("https://www.kv.ee", href)
            # proste filtrowanie: tylko kv.ee i kończące się .html (dla Twojego przykładu)
            parsed = urlparse(href)
            if "kv.ee" not in parsed.netloc:
                continue
            if href.endswith(".html"):
                urls.add(href.split("#")[0])
    print(f"Znaleziono {len(urls)} unikatowych linków do ogłoszeń (z zapisanych stron).")
    with open(LISTINGS_OUT, "w", encoding="utf-8") as out:
        for u in sorted(urls):
            out.write(u + "\n")
    print(f"URL-e zapisane w: {LISTINGS_OUT}")

# ====== 3) (OPCJONALNIE) POBRANIE KAŻDEGO OGŁOSZENIA ======
def fetch_each_listing(save_dir=os.path.join(OUT_DIR, "listings")):
    os.makedirs(save_dir, exist_ok=True)
    if not os.path.exists(LISTINGS_OUT):
        print("Brak pliku z URL-ami. Najpierw uruchom extract_listing_urls().")
        return
    with open(LISTINGS_OUT, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]
    print(f"Pobieram {len(urls)} ogłoszeń (zapisywane w {save_dir})")
    for url in urls:
        # stwórz bezpieczną nazwę pliku na podstawie końcówki URL
        name = url.rstrip("/").split("/")[-1]
        fname = os.path.join(save_dir, name + ".html")
        if os.path.exists(fname):
            print(f"-> {name} już pobrane, pomijam")
            continue
        try:
            r = session.get(url, proxies=PROXIES, timeout=20)
            print(f"Pobrałem {url} -> {r.status_code}")
            if r.status_code == 200:
                save_file(fname, r.text)
            else:
                print("Nie 200:", r.status_code)
        except Exception as e:
            print("Błąd przy pobieraniu", url, e)
        safe_sleep(0.5, 1.0)

# ====== RUN ======
if __name__ == "__main__":
    fetch_search_pages()      # pobiera wszystkie strony wyników (zapis w pages/)
    extract_listing_urls()    # wyciąga linki i zapisuje listing_urls.txt
    # jeśli chcesz, odkomentuj poniższe aby pobrać każdą stronę ogłoszenia:
    # fetch_each_listing()