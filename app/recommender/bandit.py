import random
from flask import session
from app.recommender.collaborative import get_recommendations_for_user
from app.recommender.content_based import get_similar_products_for_cart
from app.recommender.popular import get_popular_products

class EpsilonGreedyBandit:
    def __init__(self, arms, epsilon=0.7):
        self.arms = arms
        self.epsilon = epsilon

        self.counts = {arm: 0 for arm in arms}
        self.values = {arm: 0.0 for arm in arms}

    def select_arm(self):
        if random.random() < self.epsilon:
            return random.choice(self.arms)

        return max(self.values, key=self.values.get)

    def update(self, arm, reward):
        print("Strategy: ", arm)
        print("Reward: ", reward)
        self.counts[arm] += 1
        n = self.counts[arm]
        value = self.values[arm]

        self.values[arm] = value + (reward - value) / n


bandit = EpsilonGreedyBandit(
    arms=["collaborative", "content_based", "popular"]
)

def get_ai_recommendations(user_id, limit=5):
    strategy = bandit.select_arm()

    if strategy == "collaborative":
        product_ids = get_recommendations_for_user(user_id, limit)

    elif strategy == "content_based":
        products = get_similar_products_for_cart([], limit)
        product_ids = [p.id for p in products]

    else: 
        products = get_popular_products(limit)
        product_ids = [p.id for p in products]

    print(product_ids)
    return product_ids, strategy
