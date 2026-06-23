from bs4 import BeautifulSoup


class HtmlParserMoto:
    def __init__(self):
        self.html = self.get_html()
        self.soup = BeautifulSoup(self.html, "html.parser") # "lxml"

    def extract_info(self):
        price = self.get_price()
        title = self.get_title()
        description = self.get_description()
        model = self.get_model()
        milage = self.get_milage()
        fuel_type = self.get_fuel_type()
        color = self.get_color()
        production_year = self.get_production_year()
        engine_capacity = self.get_engine_capacity()
        horse_power = self.get_horse_power()
        body_style = self.get_body_style()
        registration_year = self.get_registration_year()
        location = self.get_location()
        seller_name = self.get_seller_name()
        offer_date = self.get_offer_date()
        seller_join_date = self.get_seller_join_date()
        offer_id = self.get_offer_id()
        site_name = self.get_site_name()
        photo_count = self.get_photo_count()
        data = {"price": price,
                "title": title,
                "description": description,
                "model": model,
                "milage": milage,
                "fuel_type": fuel_type,
                "color": color,
                "production_year": production_year,
                "engine_capacity": engine_capacity,
                "horse_power": horse_power,
                "body_style": body_style,
                "registration_year": registration_year,
                "location": location,
                "seller_name": seller_name,
                "offer_date": offer_date,
                "seller_join_date": seller_join_date,
                "offer_id": offer_id,
                "site_name": site_name,
                "photo_count": photo_count
                }
        return data

    def get_html(self):
        with open("example_3.html") as f:
            page_content = f.read()
        return page_content

    def get_price(self):
        """12 000 PLN"""
        price = self.soup.find("h3", class_="offer-price__number").text.replace(" ", "")
        return float(price)

    def get_title(self):
        """Żuk Inny"""
        title = self.soup.find("h1", class_="offer-title big-text eng3xoo2 ooa-ev3vab").text
        return title
    def get_description(self):
        """Samochód od 2 lat nie odpalany, wcześniej palił na dotyk, przejechał rajd Złombol. OC na rok, brał przeglądu. Więcej informacji pod telefonem
Cena do negocjacji """
        description = self.soup.find( 
            
            <div class="ooa-unlmzs e1s9vvdy4" style="margin-top:0;margin-bottom:0">
             <p>
              Samochód od 2 lat nie odpalany, wcześniej palił na dotyk, przejechał rajd Złombol. OC na rok, brał przeglądu. Więcej informacji pod telefonem
             </p>
        return description
    def get_model(self):
        """Żuk"""
        pass
    def get_milage(self):
        """65 000 km"""
        pass  <title data-next-head="">
   Używany Żuk Inny 1992 - 12 000 PLN, 65 000 km - Otomoto.pl
  </title>
    def get_fuel_type(self):
        """Benzyna+LPG"""
         <div aria-label="Rodzaj paliwa Benzyna+LPG" class="ooa-1jqwucs e127x9ub1" data-testid="detail" tabindex="0">
            <svg aria-label="Rodzaj paliwa Benzyna+LPG" class="ooa-c3wb15" fill="none" height="1em" role="img" viewbox="0 0 24 24" width="1em" xmlns="http://www.w3.org/2000/svg">
             <path d="M10.997 9H6V5h4.997z" fill="currentColor">
    def get_color(self):
        """Pomarańczowy"""
            <p class="e1nqkcyc11 ooa-ugve4x">
              Pomarańczowy
             </p>
    def get_production_year(self):
        """1992"""
           <p class="e1nqkcyc11 ooa-ugve4x">
              1992
             </p>
    def get_engine_capacity(self):
        """2 120 cm3"""
              <p class="e1nqkcyc11 ooa-ugve4x">
                  2 120 cm3
                 </p>
    def get_horse_power(self):
                 <p class="e1nqkcyc11 ooa-ugve4x">
                  71 KM
                 </p>
    def get_body_style(self):
        """Minivan"""
        pass
    def get_registration_year(self):
        """22 października 1992"""
        pass
    def get_location(self):
        """Kościerzyna, kościerski, Pomorskie"""
        pass
    def get_seller_name(self):
        """Robert"""
        pass
    def get_offer_date(self):
        """5 marca 2026 10:30"""
        pass
    def get_seller_join_date(self):
        """Sprzedający na OTOMOTO od 2025"""
        pass
    def get_condition(self):
        """Używany"""
        pass
    def get_offer_id(self):
        """6145644261"""
        pass
    def get_site_name(self):
        name = self.soup.find("meta", property="og:site_name").get("content")
        return name
    def get_photo_count(self):
        """4"""
        pass

html = HtmlParserMoto()
print(html.get_price())
