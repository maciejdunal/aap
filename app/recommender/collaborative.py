import pandas as pd
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity
from app import db
from app.models import ProductClick, Order, OrderItem

USER_PRODUCT_MATRIX = None
USER_SIMILARITY = None
USER_RECOMMENDATION_CACHE = {}

def build_recommendation_model():
    """
    Builds collaborative filtering model using:
    - clicks (weight = 1)
    - orders (weight = 5)

    Run ONCE on app startup.
    """
    global USER_PRODUCT_MATRIX, USER_SIMILARITY

    print("Building recommendation model...")

    clicks_query = db.session.query(
        ProductClick.user_id,
        ProductClick.product_id
    ).filter(ProductClick.user_id.isnot(None)).all()

    clicks_df = pd.DataFrame(clicks_query, columns=["user_id", "product_id"])
    if not clicks_df.empty:
        clicks_df["score"] = 1
        clicks_df = clicks_df.groupby(["user_id", "product_id"]).sum().reset_index()

    orders_query = db.session.query(
        Order.user_id,
        OrderItem.product_id
    ).join(OrderItem, Order.id == OrderItem.order_id).all()

    orders_df = pd.DataFrame(orders_query, columns=["user_id", "product_id"])
    if not orders_df.empty:
        orders_df["score"] = 5
        orders_df = orders_df.groupby(["user_id", "product_id"]).sum().reset_index()

    interactions = pd.concat([clicks_df, orders_df], ignore_index=True)

    if interactions.empty:
        print("⚠️ No interactions found – model not built")
        return

    matrix = interactions.pivot_table(
        index="user_id",
        columns="product_id",
        values="score",
        fill_value=0
    )

    USER_PRODUCT_MATRIX = matrix

    similarity = cosine_similarity(matrix)
    USER_SIMILARITY = pd.DataFrame(
        similarity,
        index=matrix.index,
        columns=matrix.index
    )

    print("✅ Recommendation collaborative model ready")

def get_recommendations_for_user(user_id, limit=5):
    """
    Returns product IDs recommended for given user.
    Computed lazily + cached.
    """
    if user_id in USER_RECOMMENDATION_CACHE:
        return USER_RECOMMENDATION_CACHE[user_id][:limit]

    if USER_PRODUCT_MATRIX is None or USER_SIMILARITY is None:
        return []

    if user_id not in USER_PRODUCT_MATRIX.index:
        return []

    similar_users = (
        USER_SIMILARITY[user_id]
        .drop(user_id)
        .sort_values(ascending=False)
        .head(3)
    )

    scores = defaultdict(float)

    for sim_user, weight in similar_users.items():
        for product_id, value in USER_PRODUCT_MATRIX.loc[sim_user].items():
            if USER_PRODUCT_MATRIX.loc[user_id, product_id] == 0:
                scores[product_id] += weight * value

    recommended = sorted(scores, key=scores.get, reverse=True)
    USER_RECOMMENDATION_CACHE[user_id] = recommended

    return recommended[:limit]

def clear_recommendation_cache():
    USER_RECOMMENDATION_CACHE.clear()



# W aplikacji zaimplementowano system rekomendacji oparty o collaborative filtering z 
# wykorzystaniem metod machine learning. Model analizuje interakcje użytkowników z produktami,
#  takie jak kliknięcia (waga 1) oraz zakupy (waga 5), tworząc macierz użytkownik–produkt. 
#  Na tej podstawie obliczane jest podobieństwo kosinusowe między użytkownikami, 
#  co pozwala rekomendować produkty oglądane lub kupowane przez najbardziej podobnych użytkowników. 
#  Model trenowany jest jednorazowo przy starcie aplikacji, a rekomendacje generowane są dynamicznie 
#  na żądanie użytkownika z wykorzystaniem cache w pamięci RAM. System działa w pełni po stronie serwera 
#  i jest zintegrowany z interfejsem sklepu poprzez asynchroniczne żądania AJAX.