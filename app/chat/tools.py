from app.models import CartItem, Product
from app import db

def get_cart_for_user(user_id):
    print("cart")
    items = CartItem.query.filter_by(user_id=user_id).all()

    if not items:
        return {
            "items": [],
            "total": 0.0,
            "message": "Koszyk jest pusty"
        }

    cart_items = []
    total = 0.0

    for item in items:
        price = float(item.product.price)
        subtotal = price * item.quantity
        total += subtotal

        cart_items.append({
            "product_id": item.product.id,
            "name": item.product.name,
            "quantity": item.quantity,
            "unit_price": price,
            "subtotal": subtotal
        })

    return {
        "items": cart_items,
        "total": round(total, 2)
    }


def remove_product_from_cart(user_id, product_id):
    print("delete: ", product_id)
    item = CartItem.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).first()

    if not item:
        return "Tego produktu nie ma w koszyku."

    db.session.delete(item)
    db.session.commit()
    return "Produkt usunięty z koszyka."


def add_product_to_cart(user_id, product_id):
    print("add", product_id)
    product = Product.query.get(product_id)
    print(product)
    if not product:
        return {
            "status": "error",
            "message": "Nie ma produktu o takim ID."
        }

    item = CartItem.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).first()

    if item:
        item.quantity += 1
    else:
        item = CartItem(
            user_id=user_id,
            product_id=product_id,
            quantity=1
        )
        db.session.add(item)

    db.session.commit()
    return {"status": "added"}

def get_products_for_llm(limit=15):
    products = Product.query.all()

    if not products:
        return {
            "products": [],
            "message": "Brak produktów w sklepie"
        }

    return {
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "price": float(p.price),
                "category": p.category,
                "purpose": p.purpose
            }
            for p in products
        ]
    }



TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_cart_for_user",
            "description": "Zwraca zawartość koszyka zalogowanego użytkownika",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_product_to_cart",
            "description": "Dodaje produkt do koszyka użytkownika",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "integer",
                        "description": "ID produktu"
                    }
                },
                "required": ["product_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remove_product_from_cart",
            "description": "Usuwa produkt z koszyka użytkownika",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "integer"
                    }
                },
                "required": ["product_id"]
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "get_products_for_llm",
        "description": (
            "Zwraca listę dostępnych produktów w sklepie. "
            "Użyj, gdy użytkownik pyta o polecane produkty, "
            "laptopy, prezenty lub ogólną ofertę. Dane w formie json, ID to id produktu, które określa indetyfikator produktu."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Maksymalna liczba produktów"
                }
            }
        }
    }
}
]
