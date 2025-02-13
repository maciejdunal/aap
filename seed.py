from app import create_app, db
from app.models import Watch

# Tworzymy aplikację Flask
app = create_app()

with app.app_context():
    # Tworzymy bazę danych
    db.create_all()

    # Usuwamy istniejące rekordy
    db.session.query(Watch).delete()
    db.session.commit()

    # Dodajemy zegarki z kategoriami
    watches = [
        # Zegarki Men - Luxury
        Watch(name="Citizen Eco-Drive", brand="Citizen", price=999.99, description="Solar-powered elegant watch with perpetual calendar.", image_url="citizen.jpg", sex="male", category="luxury"),
        Watch(name="Citizen Promaster", brand="Citizen", price=1199.99, description="Professional dive watch with ISO certification.", image_url="citizen.jpg", sex="male", category="luxury"),
        Watch(name="Citizen Satellite Wave", brand="Citizen", price=1999.99, description="GPS satellite timekeeping system for ultimate precision.", image_url="citizen.jpg", sex="male", category="luxury"),
        Watch(name="Emporio Armani Classic", brand="Emporio Armani", price=1299.99, description="Luxury fashion watch with stainless steel case and leather strap.", image_url="armani.jpg", sex="male", category="luxury"),
        Watch(name="Emporio Armani Diver", brand="Emporio Armani", price=1499.99, description="Elegant dive watch with water resistance up to 300m.", image_url="armani.jpg", sex="male", category="luxury"),
        Watch(name="Emporio Armani Ceramica", brand="Emporio Armani", price=1599.99, description="Premium ceramic watch with minimalist design.", image_url="armani.jpg", sex="male", category="luxury"),

        # Zegarki Men - Sport
        Watch(name="Casio G-Shock", brand="Casio", price=499.99, description="Durable sports watch with shock resistance.", image_url="casio.jpg", sex="male", category="sport"),
        Watch(name="Casio Pro Trek", brand="Casio", price=899.99, description="Outdoor adventure watch with triple sensor technology.", image_url="casio.jpg", sex="male", category="sport"),
        Watch(name="Emporio Armani Sportivo", brand="Emporio Armani", price=1399.99, description="Sporty yet elegant watch with high-performance quartz movement.", image_url="armani.jpg", sex="male", category="sport"),

        # Zegarki Women - Luxury
        Watch(name="Classic Petite Melrose", brand="Daniel Wellington", price=179.99, description="Elegant rose gold watch with a mesh strap.", image_url="dw.jpg", sex="female", category="luxury"),
        Watch(name="Antarès Interchangeable", brand="Michel Herbelin", price=399.99, description="Interchangeable straps for ultimate style.", image_url="herbelin.jpg", sex="female", category="luxury"),
        Watch(name="Golden Friend", brand="Swatch", price=139.99, description="Gold-toned elegance with a minimalist design.", image_url="swatch.jpg", sex="female", category="luxury"),

        # Zegarki Women - Sport
        Watch(name="Newport Lady", brand="Michel Herbelin", price=349.99, description="Sporty elegance with blue accents.", image_url="herbelin.jpg", sex="female", category="sport"),
        Watch(name="Skin Irony", brand="Swatch", price=129.99, description="Ultra-thin stainless steel design.", image_url="swatch.jpg", sex="female", category="sport"),
        Watch(name="Lady White", brand="Swatch", price=99.99, description="Classic white design for everyday wear.", image_url="swatch.jpg", sex="female", category="sport"),

        # Dodatkowe zegarki - Mix kategorii
        Watch(name="Citizen Chronograph", brand="Citizen", price=899.99, description="Stylish chronograph watch with stainless steel case.", image_url="citizen.jpg", sex="male", category="luxury"),
        Watch(name="City Line", brand="Michel Herbelin", price=299.99, description="Sophisticated watch with a steel bracelet.", image_url="herbelin.jpg", sex="female", category="luxury"),
    ]

    db.session.add_all(watches)
    db.session.commit()

    print("Added watches to the database!")
