import cloudscraper
from bs4 import BeautifulSoup
import time

# cloudscraper zamiast requests, aby ominąć blokady spowodowane przez cloudflare
scraper = cloudscraper.create_scraper()

all_links = set()  # Używamy zbioru (set), aby duplikaty usuwały się automatycznie

# Zakres stron (od 0 do 9500, co 50)
for start in range(0, 9500, 50):
    url = f"https://www.kv.ee/search?start={start}"
    print(f"Pobieram: {url}")

    try:
        r = scraper.get(url)
        if r.status_code != 200:
            print(f"Błąd HTTP: {r.status_code}. Przerywam lub czekam...")
            break

        soup = BeautifulSoup(r.text, "html.parser")
        
        # Licznik linków na tej konkretnej stronie
        count_before = len(all_links)

        for a in soup.find_all("a", href=True):
            href = a["href"]

            # Filtrowanie linków do ogłoszeń
            # Sprawdzamy czy ma .html i czy nie jest linkiem zewnętrznym
            if ".html" in href and "kv.ee" not in href:
                if href.startswith("/"):
                    full_link = "https://www.kv.ee" + href
                    all_links.add(full_link)

        print(f"Postęp: Znaleziono {len(all_links) - count_before} nowych linków (Suma: {len(all_links)})")

    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        break #Jeśli nagle strace połączenie z internetem, skrypt nie przestanie pracowac całkowicie, tylko zapisze to, co zdążył pobrać do tej pory

    # Krótka przerwa, żeby serwer nie zablokował za zbyt szybkie zapytania i nie uznal mnie za bota
    time.sleep(1)

print(f"\nŁącznie zebrano {len(all_links)} unikalnych ogłoszeń.")

with open("ogloszenia.txt", "w", encoding="utf-8") as f:
    for link in sorted(all_links):
        f.write(link + "\n")

print("Zapisano do pliku ogloszenia.txt")