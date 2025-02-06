from app import create_app, db
from app.models import Watch

# Tworzymy aplikację Flask
app = create_app()

# Otwieramy kontekst aplikacji
with app.app_context():
    # Sprawdzamy, czy baza istnieje
    db.create_all()

    # Czyszczenie tabeli (usuwamy wszystkie istniejące rekordy)
    db.session.query(Watch).delete()
    db.session.commit()

    # Tworzymy przykładowe zegarki
    watches = [
        Watch(name="Citizen Eco-Drive", brand="Citizen", price=999.99, description="Solar-powered elegant watch with perpetual calendar.", image_url="citizen.jpg"),
        Watch(name="Citizen Promaster", brand="Citizen", price=1199.99, description="Professional dive watch with ISO certification.", image_url="citizen.jpg"),
        Watch(name="Citizen Chronograph", brand="Citizen", price=899.99, description="Stylish chronograph watch with stainless steel case.", image_url="citizen.jpg"),
        Watch(name="Citizen Super Titanium", brand="Citizen", price=1599.99, description="Ultra-light and durable watch made of Super Titanium.", image_url="citizen.jpg"),
        Watch(name="Citizen Satellite Wave", brand="Citizen", price=1999.99, description="GPS satellite timekeeping system for ultimate precision.", image_url="citizen.jpg"),
        Watch(name="Casio G-Shock", brand="Casio", price=499.99, description="Durable sports watch with shock resistance.", image_url="casio.jpg"),
        Watch(name="Casio Edifice", brand="Casio", price=699.99, description="Modern business watch with Bluetooth connectivity.", image_url="casio.jpg"),
        Watch(name="Casio Pro Trek", brand="Casio", price=899.99, description="Outdoor adventure watch with triple sensor technology.", image_url="casio.jpg"),
        Watch(name="Casio Vintage", brand="Casio", price=199.99, description="Retro digital watch with classic LCD display.", image_url="casio.jpg"),
        Watch(name="Casio Baby-G", brand="Casio", price=349.99, description="Stylish and durable watch designed for women.", image_url="casio.jpg"),
        Watch(name="Emporio Armani Classic", brand="Emporio Armani", price=1299.99, description="Luxury fashion watch with stainless steel case and leather strap.", image_url="armani.jpg"),
        Watch(name="Emporio Armani Sportivo", brand="Emporio Armani", price=1399.99, description="Sporty yet elegant watch with high-performance quartz movement.", image_url="armani.jpg"),
        Watch(name="Emporio Armani Ceramica", brand="Emporio Armani", price=1499.99, description="Premium ceramic watch with minimalist design.", image_url="armani.jpg"),
        Watch(name="Emporio Armani Diver", brand="Emporio Armani", price=1599.99, description="Elegant dive watch with water resistance up to 300m.", image_url="armani.jpg")
    ]

    # Dodajemy nowe rekordy do bazy
    db.session.add_all(watches)
    db.session.commit()

    print("Dodano zegarki do bazy!")