# Watch Store E-commerce Application

## 📌 Opis

Projekt "Watch Store" to prosta aplikacja e-commerce do zakupu zegarków.
Pozwala użytkownikom na:

- Rejestrację i logowanie 🆕🔐
- Przeglądanie dostępnych zegarków ⌚
- Dodawanie produktów do koszyka 🛒
- Finalizowanie zamówień ✅
- Przeglądanie historii zamówień 📜
- Eksport zamówień w formacie XML 📂

---

## 🛠 Wymagania

- Python 3.x 🐍
- Flask
- SQLAlchemy
- pytest (do testów)
- MySQL (lub SQLite dla testów)

Instalacja zależności:

```sh
pip install -r requirements.txt
```

---

## 🚀 Uruchamianie aplikacji

1. Skonfiguruj bazę danych i zmienne środowiskowe.
2. Uruchom aplikację:

```sh
python app.py
```

3. Otwórz przeglądarkę i przejdź na:

```
http://127.0.0.1:5000/
```

📸 **Przykładowy ekran główny:**
![Main Page](screenshots/main_page.png)

📸 **Koszyk użytkownika:**
![Cart Page](screenshots/cart_page.png)

---

## 🔍 Testowanie aplikacji

Aby uruchomić testy jednostkowe:

```sh
pytest tests/
```

📸 **Przykładowe wykonanie testów:**
![Test Execution](screenshots/tests.png)

---

## 📦 Struktura projektu

```
project_root/
│-- app.py  # Plik główny aplikacji
│-- config.py  # Konfiguracja bazy danych
│-- models.py  # Modele SQLAlchemy
│-- routes/
│   ├── cart.py
│   ├── orders.py
│   ├── auth.py
│   ├── main.py
│-- static/
│   ├── styles.css
│   ├── images/
│-- templates/
│   ├── index.html
│   ├── cart.html
│   ├── order_history.html
│-- tests/
│   ├── test_auth.py
│   ├── test_cart.py
│   ├── test_orders.py
│-- README.md  # Dokumentacja
```

---

## 🔗 Endpointy API

| Endpoint            | Metoda | Opis                         |
| ------------------- | ------ | ---------------------------- |
| `/`                 | GET    | Strona główna                |
| `/login`            | POST   | Logowanie użytkownika        |
| `/register`         | POST   | Rejestracja użytkownika      |
| `/cart`             | GET    | Podgląd koszyka              |
| `/cart/add/<id>`    | POST   | Dodanie produktu do koszyka  |
| `/cart/remove/<id>` | POST   | Usunięcie produktu z koszyka |
| `/orders`           | GET    | Historia zamówień            |
| `/order/<id>/xml`   | GET    | Pobranie zamówienia jako XML |

---

## Podsumowanie

- Aplikacja działa na Flasku i wykorzystuje SQLAlchemy do obsługi bazy danych.
- Do testowania można użyć SQLite zamiast MySQL.
- W razie problemów sprawdź logi serwera lub uruchom aplikację w trybie debugowania:

```sh
flask run --debug
```

---

**Autor:** _Twoje Imię_ 👨‍💻
