"""
Script to seed fake click data for demonstration purposes
Run this to add some sample clicks to see the reports feature in action
"""

from app import create_app, db
from app.models import Product, ProductClick, User
from datetime import datetime, timedelta, timezone
import random

def seed_click_data():
    """Add fake click data for demonstration."""
    app = create_app()
    
    with app.app_context():
        products = Product.query.all()
        users = User.query.all()
        
        if not products:
            print("❌ No products found. Run seed.py first to create products.")
            return
        
        print(f"Found {len(products)} products and {len(users)} users")
        print("Seeding fake click data...")
        
        # Generate clicks over the last 30 days
        current_time = datetime.now(timezone.utc)
        clicks_to_add = []
        
        for days_ago in range(30):
            date = current_time - timedelta(days=days_ago)
            
            # Generate 1-10 clicks per day randomly
            num_clicks = random.randint(1, 10)
            
            for _ in range(num_clicks):
                # Pick a random product (with bias toward first few products)
                product_weights = [max(1, len(products) - i) for i in range(len(products))]
                product = random.choices(products, weights=product_weights)[0]
                
                # Sometimes use authenticated user, sometimes anonymous
                user = random.choice(users) if users and random.random() < 0.6 else None
                
                # Random time during that day
                hours_offset = random.uniform(0, 24)
                click_time = date - timedelta(hours=hours_offset)
                
                click = ProductClick(
                    product_id=product.id,
                    user_id=user.id if user else None,
                    ip_address=f"192.168.1.{random.randint(1, 255)}",
                    timestamp=click_time,
                    user_agent=random.choice([
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
                        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X)",
                        "Mozilla/5.0 (Android 11; Mobile; rv:89.0) Gecko/89.0"
                    ]),
                    referrer=random.choice([
                        None,  # Direct access
                        "https://google.com/search",
                        "https://facebook.com",
                        "https://instagram.com",
                        "https://youtube.com"
                    ])
                )
                clicks_to_add.append(click)
        
        # Add all clicks to database
        db.session.add_all(clicks_to_add)
        db.session.commit()
        
        print(f"✅ Added {len(clicks_to_add)} fake clicks!")
        
        # Show summary
        from sqlalchemy import func, desc
        top_products = (
            db.session.query(
                Product.name,
                Product.brand,
                func.count(ProductClick.id).label('clicks')
            )
            .join(ProductClick, product.id == ProductClick.product_id)
            .group_by(Product.id)
            .order_by(desc('clicks'))
            .limit(5)
            .all()
        )
        
        print("\nTop 5 most clicked products:")
        for i, (name, brand, clicks) in enumerate(top_products, 1):
            print(f"{i}. {name} ({brand}) - {clicks} clicks")
        
        total_clicks = ProductClick.query.count()
        print(f"\nTotal clicks in database: {total_clicks}")
        print("\n🎉 You can now visit /reports to see the analytics dashboard!")

if __name__ == "__main__":
    print("=== Seeding Click Data ===")
    seed_click_data()