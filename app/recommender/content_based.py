import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.models import Product
from app.models import Product, Order, OrderItem
from flask_login import current_user
from collections import defaultdict
PRODUCT_DF = None
PRODUCT_SIM = None

def build_content_model():
    global PRODUCT_DF, PRODUCT_SIM
    products = Product.query.all()

    df = pd.DataFrame([{
        "id": p.id,
        "text": f"{p.category} {p.subcategory or ''} {p.purpose or ''} {p.description}"
    } for p in products])

    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df["text"])

    similarity = cosine_similarity(tfidf_matrix)

    PRODUCT_DF = df
    PRODUCT_SIM = similarity
    print("✅ Recommendation content based model ready")


def get_similar_products_for_cart(cart_items, limit=5, max_per_category=2):
    if PRODUCT_DF is None or PRODUCT_SIM is None:
        return []

    product_ids = set()

    if cart_items:
        product_ids = {item.product_id for item in cart_items}

    else:
        if not current_user.is_authenticated:
            return []

        last_order = (
            Order.query
            .filter_by(user_id=current_user.id)
            .order_by(Order.date.desc())
            .first()
        )

        if not last_order:
            return []

        product_ids = {
            item.product_id
            for item in OrderItem.query.filter_by(order_id=last_order.id).all()
        }

    if not product_ids:
        return []

    scores = {}

    for pid in product_ids:
        idx_list = PRODUCT_DF.index[PRODUCT_DF["id"] == pid]
        if len(idx_list) == 0:
            continue

        idx = idx_list[0]
        similarities = PRODUCT_SIM[idx]

        for i in similarities.argsort()[-10:-1]:
            score = similarities[i]
            if score < 0.15:
                continue

            target_id = int(PRODUCT_DF.iloc[i]["id"])
            if target_id not in product_ids:
                scores[target_id] = scores.get(target_id, 0) + score

    if not scores:
        return []

    sorted_ids = sorted(scores, key=scores.get, reverse=True)

    category_counter = defaultdict(int)
    final_products = []

    products = Product.query.filter(Product.id.in_(sorted_ids)).all()
    product_map = {p.id: p for p in products}

    for pid in sorted_ids:
        product = product_map.get(pid)
        if not product:
            continue

        category = product.category

        if category_counter[category] >= max_per_category:
            continue

        final_products.append(product)
        category_counter[category] += 1

        if len(final_products) == limit:
            break

    return final_products


# System rekomendacji wykorzystuje sztuczną inteligencję do analizy zachowań użytkowników, takich jak przeglądanie produktów, kliknięcia oraz zakupy.
# Na podstawie tych danych identyfikowane są podobieństwa między klientami o zbliżonych zainteresowaniach.
# Następnie system proponuje produkty, które były popularne lub istotne dla innych, podobnych użytkowników.
# Dzięki temu możesz odkryć produkty dopasowane do Twojego stylu, nawet jeśli nie wyszukiwałeś ich bezpośrednio.
# Rekomendacje są na bieżąco aktualizowane wraz z nowymi interakcjami.