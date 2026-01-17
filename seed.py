from app import create_app, db
from app.models import User, Product, ProductClick
from werkzeug.security import generate_password_hash
import random
from datetime import datetime, timedelta, timezone

app = create_app()

def seed_users():
    print("Seeding users...")
    for i in range(1, 11):
        user = User(
            username=f"user{i}",
            password=generate_password_hash("user")
        )
        db.session.add(user)
    db.session.commit()
    print("✅ 10 users added")


def seed_products():
    print("Seeding products...")

    products = [

        # 💻 KOMPUTERY
        Product(
            name="PC Gaming",
            brand="Generic",
            price=6500,
            description="Powerful gaming PC",
            image_url="komputer.jpg",
            sex="unisex",
            category="Komputer",
            subcategory="gaming",
            purpose="gaming",
            specs={"cpu": "Intel i7", "ram": "32GB", "gpu": "RTX 4070", "storage": "1TB SSD"},
            rating=round(random.uniform(4.5, 4.9), 1)
        ),
        Product(
            name="PC Office",
            brand="Generic",
            price=3200,
            description="Office desktop PC",
            image_url="komputer.jpg",
            sex="unisex",
            category="Komputer",
            subcategory="office",
            purpose="work",
            specs={"cpu": "Intel i5", "ram": "16GB", "storage": "512GB SSD"},
            rating=round(random.uniform(3.9, 4.5), 1)
        ),
        Product(
            name="PC Creator",
            brand="Generic",
            price=7800,
            description="PC for content creators",
            image_url="komputer.jpg",
            sex="unisex",
            category="Komputer",
            subcategory="creator",
            purpose="work",
            specs={"cpu": "Ryzen 9", "ram": "64GB", "gpu": "RTX 4080", "storage": "2TB SSD"},
            rating=round(random.uniform(4.6, 4.9), 1)
        ),
        Product(
            name="Mini PC",
            brand="Generic",
            price=2600,
            description="Compact mini PC",
            image_url="komputer.jpg",
            sex="unisex",
            category="Komputer",
            subcategory="mini",
            purpose="office",
            specs={"cpu": "Intel i3", "ram": "8GB", "storage": "256GB SSD"},
            rating=round(random.uniform(3.8, 4.3), 1)
        ),
        Product(
            name="PC Budget",
            brand="Generic",
            price=2500,
            description="Budget desktop PC",
            image_url="komputer.jpg",
            sex="unisex",
            category="Komputer",
            subcategory="budget",
            purpose="home",
            specs={"cpu": "Ryzen 3", "ram": "8GB", "storage": "256GB SSD"},
            rating=round(random.uniform(3.7, 4.2), 1)
        ),

        # 💻 LAPTOPY
        Product(
            name="Laptop Gaming",
            brand="Generic",
            price=7200,
            description="Gaming laptop",
            image_url="laptop.jpg",
            sex="unisex",
            category="Laptop",
            subcategory="gaming",
            purpose="gaming",
            specs={"cpu": "Intel i7", "ram": "32GB", "gpu": "RTX 4060", "screen": "165Hz"},
            rating=round(random.uniform(4.4, 4.8), 1)
        ),
        Product(
            name="Laptop Business",
            brand="Generic",
            price=4800,
            description="Business laptop",
            image_url="laptop.jpg",
            sex="unisex",
            category="Laptop",
            subcategory="business",
            purpose="work",
            specs={"cpu": "Intel i5", "ram": "16GB", "storage": "512GB SSD", "weight": "1.6kg"},
            rating=round(random.uniform(4.0, 4.6), 1)
        ),
        Product(
            name="Laptop Student",
            brand="Generic",
            price=3200,
            description="Laptop for students",
            image_url="laptop.jpg",
            sex="unisex",
            category="Laptop",
            subcategory="student",
            purpose="study",
            specs={"cpu": "Ryzen 5", "ram": "8GB", "storage": "512GB SSD"},
            rating=round(random.uniform(3.8, 4.4), 1)
        ),
        Product(
            name="Laptop Ultrabook",
            brand="Generic",
            price=5500,
            description="Light ultrabook",
            image_url="laptop.jpg",
            sex="unisex",
            category="Laptop",
            subcategory="ultrabook",
            purpose="work",
            specs={"cpu": "Intel i7", "ram": "16GB", "storage": "1TB SSD", "weight": "1.3kg"},
            rating=round(random.uniform(4.3, 4.8), 1)
        ),
        Product(
            name="Laptop Multimedia",
            brand="Generic",
            price=4100,
            description="Multimedia laptop",
            image_url="laptop.jpg",
            sex="unisex",
            category="Laptop",
            subcategory="media",
            purpose="entertainment",
            specs={"cpu": "Intel i5", "ram": "16GB", "storage": "512GB SSD"},
            rating=round(random.uniform(4.0, 4.5), 1)
        ),

        # ⌨️ KLAWIATURY
        Product(name="Keyboard Mechanical", brand="Generic", price=450, description="Mechanical keyboard",
                image_url="klawiatura.jpg", sex="unisex", category="Klawiatura", purpose="gaming", rating=round(random.uniform(2.0, 4.8), 1)),
        Product(name="Keyboard Office", brand="Generic", price=150, description="Office keyboard",
                image_url="klawiatura.jpg", sex="unisex", category="Klawiatura", purpose="work", rating=round(random.uniform(2.0, 4.8), 1)),
        Product(name="Keyboard RGB", brand="Generic", price=520, description="RGB mechanical keyboard",
                image_url="klawiatura.jpg", sex="unisex", category="Klawiatura", purpose="gaming", rating=round(random.uniform(2.0, 4.8), 1)),
        Product(name="Keyboard Wireless", brand="Generic", price=260, description="Wireless keyboard",
                image_url="klawiatura.jpg", sex="unisex", category="Klawiatura", purpose="work", rating=round(random.uniform(2.0, 4.8), 1)),
        Product(name="Keyboard Compact", brand="Generic", price=300, description="Compact keyboard",
                image_url="klawiatura.jpg", sex="unisex", category="Klawiatura", purpose="home", rating=round(random.uniform(2.0, 4.8), 1)),

        # 🖱️ MYSZKI
        Product(
            name="Gaming Mouse",
            brand="Generic",
            price=250,
            description="Gaming mouse",
            image_url="myszka.jpg",
            sex="unisex",
            category="Myszka",
            purpose="gaming",
            specs={
                "dpi": 16000,
                "sensor": "optical",
                "rgb": False,
                "buttons": 6
            },
            rating=round(random.uniform(4.2, 4.7), 1)
        ),

        Product(
            name="Office Mouse",
            brand="Generic",
            price=90,
            description="Office mouse",
            image_url="myszka.jpg",
            sex="unisex",
            category="Myszka",
            purpose="work",
            specs={
                "dpi": 2400,
                "sensor": "optical",
                "wireless": False,
                "buttons": 3
            },
            rating=round(random.uniform(3.8, 4.3), 1)
        ),

        Product(
            name="Mouse Wireless",
            brand="Generic",
            price=180,
            description="Wireless mouse",
            image_url="myszka.jpg",
            sex="unisex",
            category="Myszka",
            purpose="work",
            specs={
                "dpi": 3200,
                "sensor": "optical",
                "wireless": True,
                "battery_life_months": 12
            },
            rating=round(random.uniform(4.0, 4.5), 1)
        ),

        Product(
            name="Mouse Ergonomic",
            brand="Generic",
            price=220,
            description="Ergonomic mouse",
            image_url="myszka.jpg",
            sex="unisex",
            category="Myszka",
            purpose="work",
            specs={
                "dpi": 4000,
                "sensor": "optical",
                "ergonomic": True,
                "buttons": 5
            },
            rating=round(random.uniform(4.1, 4.6), 1)
        ),

        Product(
            name="Mouse RGB",
            brand="Generic",
            price=310,
            description="RGB gaming mouse",
            image_url="myszka.jpg",
            sex="unisex",
            category="Myszka",
            purpose="gaming",
            specs={
                "dpi": 20000,
                "sensor": "optical",
                "rgb": True,
                "buttons": 8
            },
            rating=round(random.uniform(4.4, 4.9), 1)
        ),

        # 🟦 PODKŁADKI
        Product(name="Mouse Pad XL", brand="Generic", price=120, description="Large mouse pad",
                image_url="podkladka.jpg", sex="unisex", category="Podkładka", purpose="gaming",rating=round(random.uniform(2.2, 4.7), 1)),
        Product(name="Cooling Pad Laptop", brand="Generic", price=180, description="Laptop cooling pad",
                image_url="coolingpad.jpg", sex="unisex", category="Akcesoria", purpose="cooling",rating=round(random.uniform(2.2, 4.7), 1)),
        Product(name="Mouse Pad XXL", brand="Generic", price=180, description="Extra large mouse pad",
                image_url="podkladka.jpg", sex="unisex", category="Podkładka", purpose="gaming",rating=round(random.uniform(2.2, 4.7), 1)),
        Product(name="Mouse Pad Office", brand="Generic", price=70, description="Office mouse pad",
                image_url="podkladka.jpg", sex="unisex", category="Podkładka", purpose="work",rating=round(random.uniform(2.2, 4.7), 1)),
        Product(name="Cooling Pad RGB", brand="Generic", price=240, description="RGB cooling pad",
                image_url="coolingpad.jpg", sex="unisex", category="Akcesoria", purpose="gaming", rating=round(random.uniform(2.2, 4.7), 1)),

        # 🖥️ MONITORY
        Product(
            name="Monitor 144Hz",
            brand="Generic",
            price=1200,
            description="Gaming monitor",
            image_url="monitor.jpg",
            sex="unisex",
            category="Monitor",
            purpose="gaming",
            specs={
                "size": "27\"",
                "resolution": "2560x1440",
                "refresh_rate": "144Hz",
                "panel": "IPS",
                "response_time_ms": 1
            },
            rating=round(random.uniform(4.2, 4.7), 1)
        ),

        Product(
            name="Monitor Office",
            brand="Generic",
            price=800,
            description="Office monitor",
            image_url="monitor.jpg",
            sex="unisex",
            category="Monitor",
            purpose="work",
            specs={
                "size": "24\"",
                "resolution": "1920x1080",
                "refresh_rate": "75Hz",
                "panel": "IPS",
                "eye_care": True
            },
            rating=round(random.uniform(3.9, 4.4), 1)
        ),

        Product(
            name="Monitor 165Hz",
            brand="Generic",
            price=1500,
            description="High refresh gaming monitor",
            image_url="monitor.jpg",
            sex="unisex",
            category="Monitor",
            purpose="gaming",
            specs={
                "size": "27\"",
                "resolution": "2560x1440",
                "refresh_rate": "165Hz",
                "panel": "IPS",
                "response_time_ms": 1
            },
            rating=round(random.uniform(4.4, 4.9), 1)
        ),

        Product(
            name="Monitor Ultrawide",
            brand="Generic",
            price=1800,
            description="Ultrawide monitor",
            image_url="monitor.jpg",
            sex="unisex",
            category="Monitor",
            purpose="work",
            specs={
                "size": "34\"",
                "resolution": "3440x1440",
                "refresh_rate": "100Hz",
                "panel": "VA",
                "aspect_ratio": "21:9"
            },
            rating=round(random.uniform(4.1, 4.6), 1)
        ),

        Product(
            name="Monitor 4K",
            brand="Generic",
            price=2200,
            description="4K monitor",
            image_url="monitor.jpg",
            sex="unisex",
            category="Monitor",
            purpose="graphics",
            specs={
                "size": "32\"",
                "resolution": "3840x2160",
                "refresh_rate": "60Hz",
                "panel": "IPS",
                "color_coverage": "99% sRGB"
            },
            rating=round(random.uniform(4.3, 4.8), 1)
        ),


        # 🎧 SŁUCHAWKI
        Product(
            name="Gaming Headset",
            brand="Generic",
            price=600,
            description="Gaming headphones",
            image_url="sluchawki.jpg",
            sex="unisex",
            category="Słuchawki",
            subcategory="gaming",
            purpose="gaming",
            specs={
                "microphone": True,
                "surround": "7.1",
                "wireless": False,
                "frequency_response": "20Hz–20kHz"
            },
            rating=round(random.uniform(4.3, 4.8), 1)
        ),

        Product(
            name="Headphones Music",
            brand="Generic",
            price=350,
            description="Music headphones",
            image_url="sluchawki.jpg",
            sex="unisex",
            category="Słuchawki",
            subcategory="music",
            purpose="music",
            specs={
                "microphone": False,
                "wireless": False,
                "frequency_response": "18Hz–22kHz",
                "impedance_ohm": 32
            },
            rating=round(random.uniform(4.0, 4.5), 1)
        ),

        Product(
            name="Wireless Headphones",
            brand="Generic",
            price=420,
            description="Wireless headphones",
            image_url="sluchawki.jpg",
            sex="unisex",
            category="Słuchawki",
            subcategory="wireless",
            purpose="music",
            specs={
                "wireless": True,
                "bluetooth": "5.2",
                "battery_hours": 30,
                "microphone": True
            },
            rating=round(random.uniform(4.1, 4.6), 1)
        ),

        Product(
            name="Studio Headphones",
            brand="Generic",
            price=680,
            description="Studio headphones",
            image_url="sluchawki.jpg",
            sex="unisex",
            category="Słuchawki",
            subcategory="studio",
            purpose="music",
            specs={
                "wireless": False,
                "frequency_response": "10Hz–40kHz",
                "impedance_ohm": 80,
                "open_back": True
            },
            rating=round(random.uniform(4.4, 4.9), 1)
        ),

        Product(
            name="Office Headset",
            brand="Generic",
            price=300,
            description="Office headset",
            image_url="sluchawki.jpg",
            sex="unisex",
            category="Słuchawki",
            subcategory="office",
            purpose="work",
            specs={
                "microphone": True,
                "wireless": True,
                "noise_cancelling": True,
                "battery_hours": 20
            },
            rating=round(random.uniform(3.9, 4.4), 1)
        ),



        # ⌚ ZEGARKI
        Product(
            name="Classic Watch",
            brand="Generic",
            price=500,
            description="Classic watch",
            image_url="zegarek.jpg",
            sex="male",
            category="Zegarek",
            purpose="fashion",
            specs={
                "mechanism": "quartz",
                "water_resistance": "5 ATM",
                "case_material": "stainless steel"
            },
            rating=round(random.uniform(4.0, 4.5), 1)
        ),

        Product(
            name="Smartwatch",
            brand="Generic",
            price=900,
            description="Smartwatch",
            image_url="smartwatch.jpg",
            sex="unisex",
            category="Smartwatch",
            purpose="sport",
            specs={
                "gps": True,
                "heart_rate": True,
                "steps": True,
                "battery_days": 7
            },
            rating=round(random.uniform(4.1, 4.6), 1)
        ),

        Product(
            name="Fitness Band",
            brand="Generic",
            price=300,
            description="Fitness band",
            image_url="opaska.jpg",
            sex="unisex",
            category="Opaska",
            purpose="fitness",
            specs={
                "heart_rate": True,
                "steps": True,
                "sleep_tracking": True,
                "battery_days": 14
            },
            rating=round(random.uniform(3.9, 4.4), 1)
        ),

        Product(
            name="Luxury Watch",
            brand="Generic",
            price=1200,
            description="Luxury classic watch",
            image_url="zegarek.jpg",
            sex="male",
            category="Zegarek",
            purpose="fashion",
            specs={
                "mechanism": "automatic",
                "water_resistance": "10 ATM",
                "case_material": "sapphire glass"
            },
            rating=round(random.uniform(4.3, 4.8), 1)
        ),

        Product(
            name="Kids Smartwatch",
            brand="Generic",
            price=400,
            description="Smartwatch for kids",
            image_url="smartwatch.jpg",
            sex="unisex",
            category="Smartwatch",
            purpose="kids",
            specs={
                "gps": True,
                "calling": True,
                "parent_control": True,
                "battery_days": 3
            },
            rating=round(random.uniform(3.8, 4.3), 1)
        ),

        Product(
            name="Sport Smartwatch",
            brand="Generic",
            price=1100,
            description="Advanced sport smartwatch",
            image_url="smartwatch.jpg",
            sex="unisex",
            category="Smartwatch",
            purpose="sport",
            specs={
                "gps": True,
                "heart_rate": True,
                "vo2max": True,
                "water_resistance": "10 ATM",
                "battery_days": 10
            },
            rating=round(random.uniform(4.4, 4.9), 1)
        ),

        # 💾 PODZESPOŁY
        Product(
            name="SSD 1TB",
            brand="Generic",
            price=450,
            description="SSD disk",
            image_url="ssd.jpg",
            sex="unisex",
            category="Dysk",
            purpose="storage",
            specs={
                "capacity": "1TB",
                "interface": "NVMe",
                "read_speed": "3500MB/s",
                "write_speed": "3000MB/s"
            },
            rating=round(random.uniform(4.2, 4.7), 1)
        ),

        Product(
            name="RAM 16GB",
            brand="Generic",
            price=320,
            description="RAM memory",
            image_url="ram.jpg",
            sex="unisex",
            category="RAM",
            purpose="upgrade",
            specs={
                "capacity": "16GB",
                "type": "DDR4",
                "speed": "3200MHz"
            },
            rating=round(random.uniform(4.0, 4.5), 1)
        ),

        Product(
            name="Graphics Card",
            brand="Generic",
            price=2800,
            description="GPU card",
            image_url="gpu.jpg",
            sex="unisex",
            category="GPU",
            purpose="gaming",
            specs={
                "vram": "12GB",
                "architecture": "Ampere",
                "ray_tracing": True
            },
            rating=round(random.uniform(4.4, 4.9), 1)
        ),

        Product(
            name="SSD 2TB",
            brand="Generic",
            price=850,
            description="2TB SSD disk",
            image_url="ssd.jpg",
            sex="unisex",
            category="Dysk",
            purpose="storage",
            specs={
                "capacity": "2TB",
                "interface": "NVMe",
                "read_speed": "5000MB/s",
                "write_speed": "4500MB/s"
            },
            rating=round(random.uniform(4.5, 4.9), 1)
        ),

        Product(
            name="RAM 32GB",
            brand="Generic",
            price=650,
            description="32GB RAM memory",
            image_url="ram.jpg",
            sex="unisex",
            category="RAM",
            purpose="upgrade",
            specs={
                "capacity": "32GB",
                "type": "DDR4",
                "speed": "3600MHz"
            },
            rating=round(random.uniform(4.3, 4.8), 1)
        ),

        Product(
            name="GPU Budget",
            brand="Generic",
            price=1800,
            description="Budget graphics card",
            image_url="gpu.jpg",
            sex="unisex",
            category="GPU",
            purpose="gaming",
            specs={
                "vram": "8GB",
                "architecture": "Turing",
                "ray_tracing": False
            },
            rating=round(random.uniform(4.0, 4.4), 1)
        ),


        # 📺 RTV
        Product(
            name="Smart TV 55",
            brand="Generic",
            price=3200,
            description="Smart television",
            image_url="tv.jpg",
            sex="unisex",
            category="Telewizor",
            purpose="entertainment",
            specs={
                "size": "55\"",
                "resolution": "4K",
                "panel": "LED",
                "hdr": True,
                "smart_tv": True,
                "refresh_rate": "60Hz"
            },
            rating=round(random.uniform(4.1, 4.6), 1)
        ),

        Product(
            name="Smart TV 65",
            brand="Generic",
            price=4200,
            description="65 inch Smart TV",
            image_url="tv.jpg",
            sex="unisex",
            category="Telewizor",
            purpose="entertainment",
            specs={
                "size": "65\"",
                "resolution": "4K",
                "panel": "LED",
                "hdr": True,
                "smart_tv": True,
                "refresh_rate": "120Hz"
            },
            rating=round(random.uniform(4.3, 4.7), 1)
        ),

        Product(
            name="OLED TV",
            brand="Generic",
            price=6500,
            description="OLED television",
            image_url="tv.jpg",
            sex="unisex",
            category="Telewizor",
            purpose="cinema",
            specs={
                "size": "65\"",
                "resolution": "4K",
                "panel": "OLED",
                "hdr": True,
                "dolby_vision": True,
                "refresh_rate": "120Hz"
            },
            rating=round(random.uniform(4.6, 4.9), 1)
        ),

        Product(
            name="TV Budget",
            brand="Generic",
            price=2200,
            description="Budget Smart TV",
            image_url="tv.jpg",
            sex="unisex",
            category="Telewizor",
            purpose="home",
            specs={
                "size": "50\"",
                "resolution": "4K",
                "panel": "LED",
                "hdr": False,
                "smart_tv": True,
                "refresh_rate": "60Hz"
            },
            rating=round(random.uniform(3.8, 4.3), 1)
        ),


        # 🏠 AGD
        Product(
            name="Fridge",
            brand="Generic",
            price=2800,
            description="Refrigerator",
            image_url="lodowka.jpg",
            sex="unisex",
            category="AGD",
            subcategory="kitchen",
            purpose="home",
            specs={
                "capacity_l": 350,
                "energy_class": "A++",
                "no_frost": True,
                "freezer": True
            },
            rating=round(random.uniform(4.0, 4.5), 1)
        ),

        Product(
            name="Washing Machine",
            brand="Generic",
            price=2600,
            description="Washing machine",
            image_url="pralka.jpg",
            sex="unisex",
            category="AGD",
            subcategory="laundry",
            purpose="home",
            specs={
                "capacity_kg": 9,
                "energy_class": "A+++",
                "rpm": 1400,
                "steam": True
            },
            rating=round(random.uniform(4.1, 4.6), 1)
        ),

        Product(
            name="Oven",
            brand="Generic",
            price=2400,
            description="Oven",
            image_url="piekarnik.jpg",
            sex="unisex",
            category="AGD",
            subcategory="kitchen",
            purpose="home",
            specs={
                "type": "electric",
                "capacity_l": 70,
                "convection": True,
                "self_cleaning": True
            },
            rating=round(random.uniform(4.0, 4.5), 1)
        ),

        Product(
            name="Dishwasher",
            brand="Generic",
            price=2700,
            description="Dishwasher",
            image_url="zmywarka.jpg",
            sex="unisex",
            category="AGD",
            subcategory="kitchen",
            purpose="home",
            specs={
                "place_settings": 14,
                "energy_class": "A++",
                "water_saving": True,
                "noise_db": 44
            },
            rating=round(random.uniform(4.1, 4.6), 1)
        ),

        Product(
            name="Microwave",
            brand="Generic",
            price=900,
            description="Microwave oven",
            image_url="mikrofala.jpg",
            sex="unisex",
            category="AGD",
            subcategory="kitchen",
            purpose="home",
            specs={
                "power_w": 900,
                "capacity_l": 25,
                "grill": True
            },
            rating=round(random.uniform(3.8, 4.3), 1)
        ),

        Product(
            name="Dryer",
            brand="Generic",
            price=3100,
            description="Clothes dryer",
            image_url="suszarka.jpg",
            sex="unisex",
            category="AGD",
            subcategory="laundry",
            purpose="home",
            specs={
                "capacity_kg": 8,
                "energy_class": "A++",
                "heat_pump": True
            },
            rating=round(random.uniform(4.2, 4.7), 1)
        ),



        # 💡 INNE (żeby AI rozróżniało typy klientów)
        Product(
            name="LED Lamp Desk",
            brand="Generic",
            price=150,
            description="Desk lamp",
            image_url="lampa.jpg",
            sex="unisex",
            category="Oświetlenie",
            purpose="work",
            specs={
                "brightness_lm": 800,
                "color_temp": "4000K",
                "dimmable": True
            },
            rating=round(random.uniform(4.0, 4.5), 1)
        ),

        Product(
            name="LED Strip RGB",
            brand="Generic",
            price=200,
            description="RGB LED strip",
            image_url="led.jpg",
            sex="unisex",
            category="Oświetlenie",
            purpose="gaming",
            specs={
                "rgb": True,
                "length_m": 5,
                "smart_control": True
            },
            rating=round(random.uniform(4.2, 4.7), 1)
        ),

        Product(
            name="Smart LED Bulb",
            brand="Generic",
            price=120,
            description="Smart LED bulb",
            image_url="led.jpg",
            sex="unisex",
            category="Oświetlenie",
            purpose="smart_home",
            specs={
                "smart": True,
                "brightness_lm": 900,
                "color_temp_range": "2700–6500K"
            },
            rating=round(random.uniform(4.1, 4.6), 1)
        ),

        Product(
            name="Floor Lamp",
            brand="Generic",
            price=350,
            description="Floor lamp",
            image_url="lampa.jpg",
            sex="unisex",
            category="Oświetlenie",
            purpose="home",
            specs={
                "brightness_lm": 1500,
                "color_temp": "3000K",
                "height_cm": 170
            },
            rating=round(random.uniform(3.9, 4.4), 1)
        ),

        Product(
            name="Gaming Neon Light",
            brand="Generic",
            price=280,
            description="Gaming neon light",
            image_url="led.jpg",
            sex="unisex",
            category="Oświetlenie",
            purpose="gaming",
            specs={
                "rgb": True,
                "smart_control": True,
                "mount": "wall"
            },
            rating=round(random.uniform(4.3, 4.8), 1)
        ),

    ]

    db.session.add_all(products)
    db.session.commit()
    print(f"✅ {len(products)} products added")

def seed_office_user(username, ip):
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f"❌ {username} not found")
        return

    office_products = Product.query.filter(
        Product.purpose.in_(["work", "office", "study", "home"])
    ).all()

    if not office_products:
        print("❌ No office products found")
        return

    now = datetime.utcnow()
    clicks = []

    for _ in range(30):
        product = random.choice(office_products)

        click = ProductClick(
            user_id=user.id,
            product_id=product.id,
            timestamp=now - timedelta(
                days=random.randint(0, 14),
                minutes=random.randint(0, 1440)
            ),
            ip_address=ip,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            referrer=random.choice([
                "https://google.com",
                "https://linkedin.com",
                None
            ])
        )
        clicks.append(click)

    db.session.add_all(clicks)
    db.session.commit()
    print(f"✅ Added {len(clicks)} office clicks for {username}")

def seed_gamer_user(username, ip):
    user = User.query.filter_by(username=username).first()

    if not user:
        print(f"❌ {username} not found")
        return

    gamer_products = Product.query.filter(
        Product.purpose.in_(["gaming", "entertainment"])
    ).all()

    if not gamer_products:
        print("❌ No gaming products found")
        return

    now = datetime.utcnow()
    clicks = []

    for _ in range(30):
        product = random.choice(gamer_products)

        click = ProductClick(
            user_id=user.id,
            product_id=product.id,
            timestamp=now - timedelta(
                days=random.randint(0, 14),
                minutes=random.randint(0, 1440)
            ),
            ip_address=ip,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            referrer=random.choice([
                "https://google.com",
                "https://youtube.com",
                "https://twitch.tv",
                None
            ])
        )

        clicks.append(click)

    db.session.add_all(clicks)
    db.session.commit()

    print(f"✅ Added {len(clicks)} gamer clicks for {username}")

def seed_home_user(username, ip):
    user = User.query.filter_by(username=username).first()

    if not user:
        print(f"❌ {username} not found")
        return

    home_products = Product.query.filter(
        Product.purpose.in_(["home", "entertainment", "smart_home"])
    ).all()

    if not home_products:
        print("❌ No home products found")
        return

    now = datetime.utcnow()
    clicks = []

    for _ in range(30):
        product = random.choice(home_products)

        click = ProductClick(
            user_id=user.id,
            product_id=product.id,
            timestamp=now - timedelta(
                days=random.randint(0, 21),
                minutes=random.randint(0, 1440)
            ),
            ip_address=ip,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            referrer=random.choice([
                "https://google.com",
                "https://facebook.com",
                None
            ])
        )
        clicks.append(click)

    db.session.add_all(clicks)
    db.session.commit()

    print(f"✅ Added {len(clicks)} home clicks for {username}")

def seed_student_user():
    with app.app_context():
        user = User.query.filter_by(username="user7").first()

        if not user:
            print("❌ user7 not found")
            return

        student_products = Product.query.filter(
            Product.purpose.in_(["study", "work", "entertainment", "home"])
        ).all()

        if not student_products:
            print("❌ No student products found")
            return

        now = datetime.utcnow()
        clicks = []

        for _ in range(30):
            product = random.choice(student_products)

            click = ProductClick(
                user_id=user.id,
                product_id=product.id,
                timestamp=now - timedelta(
                    days=random.randint(0, 21),
                    minutes=random.randint(0, 1440)
                ),
                ip_address="192.168.0.16",
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                referrer=random.choice([
                    "https://google.com",
                    "https://youtube.com",
                    None
                ])
            )

            clicks.append(click)

        db.session.add_all(clicks)
        db.session.commit()

        print(f"✅ Added {len(clicks)} student clicks for user7")

def seed_sport_user():
    with app.app_context():
        user = User.query.filter_by(username="user8").first()

        if not user:
            print("❌ user8 not found")
            return

        sport_products = Product.query.filter(
            Product.purpose.in_(["sport", "fitness", "health", "entertainment"])
        ).all()

        if not sport_products:
            print("❌ No sport products found")
            return

        now = datetime.utcnow()
        clicks = []

        for _ in range(30):
            product = random.choice(sport_products)

            click = ProductClick(
                user_id=user.id,
                product_id=product.id,
                timestamp=now - timedelta(
                    days=random.randint(0, 21),
                    minutes=random.randint(0, 1440)
                ),
                ip_address="192.168.0.17",
                user_agent="Mozilla/5.0 (Android 13; Mobile)",
                referrer=random.choice([
                    "https://google.com",
                    "https://instagram.com",
                    None
                ])
            )

            clicks.append(click)

        db.session.add_all(clicks)
        db.session.commit()

        print(f"✅ Added {len(clicks)} sport clicks for user8")

def seed_tech_user():
    with app.app_context():
        user = User.query.filter_by(username="user9").first()

        if not user:
            print("❌ user9 not found")
            return

        tech_products = Product.query.filter(
            Product.purpose.in_([
                "gaming",
                "upgrade",
                "storage",
                "graphics",
                "entertainment",
                "smart_home"
            ])
        ).all()

        if not tech_products:
            print("❌ No tech products found")
            return

        now = datetime.utcnow()
        clicks = []

        for _ in range(30):
            product = random.choice(tech_products)

            click = ProductClick(
                user_id=user.id,
                product_id=product.id,
                timestamp=now - timedelta(
                    days=random.randint(0, 21),
                    minutes=random.randint(0, 1440)
                ),
                ip_address="192.168.0.18",
                user_agent="Mozilla/5.0 (X11; Linux x86_64)",
                referrer=random.choice([
                    "https://google.com",
                    "https://reddit.com/r/tech",
                    "https://youtube.com",
                    None
                ])
            )

            clicks.append(click)

        db.session.add_all(clicks)
        db.session.commit()

        print(f"✅ Added {len(clicks)} tech clicks for user9")

def seed_random_user():
    with app.app_context():
        user = User.query.filter_by(username="user10").first()

        if not user:
            print("❌ user10 not found")
            return

        products = Product.query.all()

        if not products:
            print("❌ No products found")
            return

        now = datetime.utcnow()
        clicks = []

        for _ in range(30):
            product = random.choice(products)

            click = ProductClick(
                user_id=user.id,
                product_id=product.id,
                timestamp=now - timedelta(
                    days=random.randint(0, 30),
                    minutes=random.randint(0, 1440)
                ),
                ip_address="192.168.0.19",
                user_agent=random.choice([
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X)",
                    "Mozilla/5.0 (Android 13; Mobile)"
                ]),
                referrer=random.choice([
                    "https://google.com",
                    "https://facebook.com",
                    "https://youtube.com",
                    None
                ])
            )

            clicks.append(click)

        db.session.add_all(clicks)
        db.session.commit()

        print(f"✅ Added {len(clicks)} random clicks for user10")

if __name__ == "__main__":
    with app.app_context():
        print("=== FULL SEED START ===")
        db.drop_all()
        db.create_all()
        seed_users()
        seed_products()
        seed_gamer_user("user1", "192.168.0.10")
        seed_gamer_user("user2", "192.168.0.11")
        seed_office_user("user3", "192.168.0.12")
        seed_office_user("user4", "192.168.0.13")
        seed_home_user("user5", "192.168.0.14")
        seed_home_user("user6", "192.168.0.15")
        seed_student_user()
        seed_sport_user()
        seed_tech_user()
        seed_random_user()
        print("=== FULL SEED DONE ===")
