from app.models import Product
from app import db
from sqlalchemy import func

def get_popular_products(limit=5):
    return (
        db.session.query(Product)
        .order_by(Product.rating.desc())
        .limit(limit)
        .all()
    )
