#lxml
#beautifulsoup4
"""
from bs4 import BeautifulSoup

with open('/Users/drizzleinthebottle/Documents/1 rok ads/semestr 2/ekstrakcja danych/repozytorium/folder1/example_1.html') as f:
    html = f.read()
print(html)
soup = BeautifulSoup(html, "lxml")
print(type(soup))

extracted = soup.find_all("div", class_="container").parent

print(extracted)
"""
"""
TERAZ ZADANIE NA WYCIAGNIECIE HTML 2
CZYLI MAMY WYCIAGNAC
USOS
19.03.2026
NAJLEPSZY KURS
"""
"""
from bs4 import BeautifulSoup

with open('/Users/drizzleinthebottle/Documents/1 rok ads/semestr 2/ekstrakcja danych/repozytorium/folder1/example_2.html') as f:
    html = f.read()

soup = BeautifulSoup(html, "lxml")

usosowski = soup.find("a").text
data = soup.find("div", class_="date").text.strip()
wyboldowany = soup.find("b").text.strip()

print(usosowski)
print(data)
print(wyboldowany)
"""
"""
TERAZ
TO CO JEST ZAPISANE WYZEJ
MA BYC ZAPISANE JAKO FUNKCJA W PYTHONIE
ROZWIAZANIE:
"""

from bs4 import BeautifulSoup

def usoslink(soup):
    tag = soup.find("a")
    return tag.text if tag else None

def data(soup):
    tag = soup.find("div", class_="date")
    return tag.text.strip() if tag else None

def boldowany(soup):
    tag = soup.find("b")
    return tag.text.strip() if tag else None

# użycie:
with open('/Users/drizzleinthebottle/Documents/1 rok ads/semestr 2/ekstrakcja danych/repozytorium/folder1/example_2.html') as f:
    html = f.read()

soup = BeautifulSoup(html, "lxml")

usos = usoslink(soup)
date = data(soup)
desc = boldowany(soup)

print(usos)
print(date)
print(desc)



