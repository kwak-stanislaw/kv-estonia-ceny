
import cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()

listing_links = []

for start in range(0, 24290, 50):

    url = f"https://www.kv.ee/search?start={start}"
    print("Pobieram:", url)

    r = scraper.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.find_all("a", href=True):

        href = a["href"]

        if ".html" in href:

            if href.startswith("/"):
                href = "https://www.kv.ee" + href

            listing_links.append(href)

# USUWAMY DUPLIKATY
listing_links = list(set(listing_links))

print("Unikalnych linków:", len(listing_links))


# zapis do pliku
with open("ogloszenia.txt", "w") as f:
    for link in listing_links:
        f.write(link + "\n")

print("Zapisane!")