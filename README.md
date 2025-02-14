# Watch Store E-commerce Application

## Opis aplikacji

Projekt **Watch Store** to prosta aplikacja e-commerce umożliwiająca zakup zegarków online.  
Pozwala użytkownikom na:

- **Rejestrację i logowanie**
- **Przeglądanie dostępnych zegarków**
- **Przeglądanie zegarków w danych kategoriach**
- **Dodawanie produktów do koszyka**
- **Podgląd koszyka**
- **Finalizowanie zamówień**
- **Przeglądanie historii zamówień**
- **Eksport zamówień w formacie XML**
- **Podgląd listy posiadanych zegarków, na podstawie historii zamówień**

---

## 🛠 Wymagania

Aby uruchomić aplikację, wymagane są:

- **Python w wersji min. 3.x**
- **Flask**
- **SQLAlchemy**
- **pytest** (do testów)
- **SQLite** (domyślna baza danych)

Instalacja zależności:

```sh
pip install -r requirements.txt
```

---

## Uruchamianie aplikacji

1️. **Skonfigurowanie bazy danych**:

```sh
python seed.py
```

2️. **Uruchomienie aplikację**:

```sh
python app.py
```

3️. **Otworzenie wygenerowanego linku, standardowo powinno to być**:

```
http://127.0.0.1:5000/
```

---

## Dokumentacja zdjęciowa

Aby lepiej zrozumieć działanie aplikacji, poniżej znajdują się zrzuty ekranu przedstawiające jej kluczowe funkcjonalności.

### **Rejestracja**

![Main Page](screenshots/register.jpg)

### **Logowanie**

![Main Page](screenshots/login.jpg)

### **Strona główna**

![Main Page](screenshots/home.jpg)

### **Filtrowanie po kategorii produktow**

![Cart Page](screenshots/sport-category.jpg)

### **Koszyk użytkownika**

![Cart Page](screenshots/cart.jpg)

### **Checkout**

![Cart Page](screenshots/checkout.jpg)

### **Historia zamówień**

![Orders Page](screenshots/orders.jpg)

### **Eksport zamówienia do XML**

![XML Export](screenshots/xml.jpg)

---

## Testowanie aplikacji

Aby uruchomić testy jednostkowe, skorzystaj z poniższego polecenia:

```sh
pytest tests/
```

![Tests Execution](screenshots/tests_execution.jpg)

---

## Struktura projektu

```
aap/
│-- app.py                   # Główna aplikacja Flask
│-- models.py                # Modele SQLAlchemy
│-- routes/
│   ├── routes.py            # Home page
│   ├── auth_routes.py       # Logowanie i rejestracja
│   ├── cart_routes.py       # Obsługa koszyka
│   ├── orders_routes.py     # Historia zamówień
│   ├── checkout_routes.py   # Finalizacja zamówienia
│   ├── my_watches_routes.py # Kupione zegarki
│-- static/
│   ├── styles.css           # Plik stylów
│-- templates/
│   ├── index.html           # Strona główna
│   ├── cart.html            # Koszyk
│   ├── checkout.html        # Finalizacja zamówienia
│   ├── orders.html          # Historia zamówień
│   ├── my_watches.html      # Kupione zegarki
│-- tests/
│   ├── test_cart.py         # Testy koszyka
│   ├── test_login.py        # Testy logowania
│   ├── test_orders.py       # Testy zamówień
│   ├── test_register.py     # Testy rejestracji
│-- requirements.txt         # Lista zależności
│-- README.md                # Dokumentacja
│-- seed.py                  # Skrypt inicjalizujący seedy do bazy danych
```

---

## Endpointy API

| Endpoint            | Metoda | Opis                         |
| ------------------- | ------ | ---------------------------- |
| `/`                 | GET    | Strona główna                |
| `/login`            | POST   | Logowanie użytkownika        |
| `/register`         | POST   | Rejestracja użytkownika      |
| `/cart`             | GET    | Podgląd koszyka              |
| `/cart/add/<id>`    | POST   | Dodanie produktu do koszyka  |
| `/cart/remove/<id>` | POST   | Usunięcie produktu z koszyka |
| `/orders`           | GET    | Historia zamówień            |
| `/orders/<id>/xml`  | GET    | Pobranie zamówienia jako XML |

---
