import requests
from bs4 import BeautifulSoup

listing_links = []

# pętla po stronach wyszukiwania
for start in range(0, 24290, 50):

    url = f"https://www.kv.ee/search?start={start}"
    print("Pobieram:", url)

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    # szukamy wszystkich linków na stronie
    for a in soup.find_all("a", href=True):

        link = a["href"]

        # szukanie ogloszen
        if ".html" in link and "search" not in link:

            if link.startswith("/"):
                link = "https://www.kv.ee" + link

            listing_links.append(link)


print("Znaleziono ogłoszeń:", len(listing_links))


# zapis do pliku
with open("ogloszenia.txt", "w") as f:
    for link in listing_links:
        f.write(link + "\n")

print("Linki do ogłoszeń zapisane")