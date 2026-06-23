import requests

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15',
    'Accept-Language': 'pl-PL,pl;q=0.9',
    'Sec-Fetch-Dest': 'document',
    'Priority': 'u=0, i',
}


req = requests.get('https://www.kv.ee/search', headers=headers)

#url = "https://www.kv.ee/search?deal_type=1"
#req = requests.get(url)

print(req.text)
print(req.status_code)

with open("estonia_ha.txt", "w", encoding="utf-8") as f:
    f.write(req.text) #zeby ominac jakąś tam blokade to wystarczy sobie proxy ustawic - a co to proxy to chyh wie
    

for i in range(1, 2046):


    