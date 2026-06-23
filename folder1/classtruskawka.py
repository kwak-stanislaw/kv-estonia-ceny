class Truskawka: 
    def __init__(self, kolor): #To jest konstruktor – specjalna funkcja, która uruchamia się automatycznie, gdy tworzymy nową truskawkę.
        self.kolor = kolor
    def dojrzewanie(self):
        self.kolor = "czerwona"
    def jaki_kolor_truskawki(self):
        return self.kolor
    def baza_truskawek(self):
        print("baza truskawek", self.kolor)
        print(self.kolor)

t = Truskawka("zielona") #tworzy nową truskawkę, ustawia jej kolor na "zielona"

#dszieki self mozna wywolywac obiekty z klasy - a mega prostym jezykiem japierdole - chodzi o to ze tą konkretną truskawke mozna wywolac
print(type(t))
print(t.kolor)
t.kolor = "czerwona"
print(t.kolor)

#czym sa selfy, czym jest konstruktor, i klasa nazywa sie z DUZEJ literki, funkcja z malej i dajemy podkreslnik, a klasa z dwoch slow zlozona - PoleTruskawek