from app import create_app, db
from app.models import User, Product, Order, OrderItem
from datetime import datetime, timedelta
import random

app = create_app()

USER_PROFILES = {
    "user1": ["gaming"],
    "user2": ["gaming"],
    "user3": ["work"],
    "user4": ["work"],
    "user5": ["home"],
    "user6": ["home"],
    "user7": ["study", "entertainment"],
    "user8": ["sport", "fitness"],
    "user9": ["upgrade", "storage", "gaming"],
    "user10": []  # random
}

def create_order(user, products):
    if not products:
        return

    total_price = sum(p.price for p in products)

    order = Order(
        user_id=user.id,
        date=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
        total_price=total_price
    )
    db.session.add(order)
    db.session.flush()

    for product in products:
        item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=random.randint(2, 5)
        )
        db.session.add(item)

def run():
    with app.app_context():
        users = {u.username: u for u in User.query.all()}
        products = Product.query.all()

        for username, purposes in USER_PROFILES.items():
            user = users.get(username)
            if not user:
                continue

            orders_count = random.randint(1, 3)

            for _ in range(orders_count):
                if purposes:
                    pool = [p for p in products if p.purpose in purposes]
                else:
                    pool = products  # random user

                if not pool:
                    continue

                order_products = random.sample(
                    pool,
                    k=random.randint(1, min(3, len(pool)))
                )

                create_order(user, order_products)

            print(f"✅ {username}: {orders_count} orders created")

        db.session.commit()
        print("🎉 Orders seeding completed!")

if __name__ == "__main__":
    run()
