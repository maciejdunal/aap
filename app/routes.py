from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import Product, OrderItem, Order, ProductClick, CartItem, db
from sqlalchemy import func, desc
from datetime import datetime, timedelta, timezone
from flask_login import current_user
from app.recommender.collaborative import get_recommendations_for_user
from app.models import Product
from sqlalchemy import distinct
from sqlalchemy import or_
from app.recommender.bandit import get_ai_recommendations
from flask import session
main = Blueprint('main', __name__)

def get_recommendations(limit=4):
    """Get product recommendations based on user's interested brands."""
    interested_brands = set()

    def extract_brands(query_result):
        return {b[0] for b in query_result}

    if current_user.is_authenticated:
        user_click_brands = db.session.query(Product.brand)\
            .join(ProductClick, Product.id == ProductClick.product_id)\
            .filter(ProductClick.user_id == current_user.id)\
            .distinct().all()
        interested_brands.update(extract_brands(user_click_brands))
        
        cart_brands = db.session.query(Product.brand)\
            .join(CartItem, Product.id == CartItem.product_id)\
            .filter(CartItem.user_id == current_user.id)\
            .distinct().all()
        interested_brands.update(extract_brands(cart_brands))

        order_brands = db.session.query(Product.brand)\
            .join(OrderItem, Product.id == OrderItem.product_id)\
            .join(Order, OrderItem.order_id == Order.id)\
            .filter(Order.user_id == current_user.id)\
            .distinct().all()
        interested_brands.update(extract_brands(order_brands))
    else:
        ip_address = request.remote_addr
        
        ip_click_brands = db.session.query(Product.brand)\
            .join(ProductClick, Product.id == ProductClick.product_id)\
            .filter(ProductClick.ip_address == ip_address)\
            .distinct().all()
        interested_brands.update(extract_brands(ip_click_brands))
    
    if not interested_brands:
        return []

    recommended = Product.query.filter(Product.brand.in_(interested_brands))\
        .order_by(func.random())\
        .limit(limit)\
        .all()
        
    return recommended

@main.route('/api/recommendations-html')
def get_recommendations_html():

    if not current_user.is_authenticated:
        return '', 204

    product_ids, strategy = get_ai_recommendations(
        user_id=current_user.id,
        limit=4
    )
    print(strategy)
   
    if not product_ids:
        return '', 204

    products = (
        Product.query
        .filter(Product.id.in_(product_ids))
        .all()
    )
    
    return render_template(
        "partials/recommendations.html",
        recommendations=products,
        strategy=strategy
    )

def get_top_selling_products(limit=4, days=30):
    """Get top selling products based on sales in the last N days."""
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    top_products = (
        db.session.query(
            Product,
            func.sum(OrderItem.quantity).label('total_sold'),
            func.count(OrderItem.id).label('order_count')
        )
        .join(OrderItem, Product.id == OrderItem.product_id)
        .join(Order, OrderItem.order_id == Order.id)
        .filter(Order.date >= cutoff_date)
        .group_by(Product.id)
        .order_by(desc('total_sold'))
        .limit(limit)
        .all()
    )
    
    if not top_products:
        fallback_products = (
            Product.query
            .order_by(desc(Product.id))
            .limit(limit)
            .all()
        )

        return [(product, 0, 0) for product in fallback_products]
    
    return top_products

from sqlalchemy import distinct

@main.route('/')
def index():

    category = request.args.get('category', 'all')
    search_query = request.args.get('search', '').strip()
    show_top = request.args.get('show_top', 'true').lower() == 'true'

    categories = [
        c[0] for c in
        db.session.query(distinct(Product.category))
        .filter(Product.category.isnot(None))
        .order_by(Product.category)
        .all()
    ]

    products_query = Product.query

    if category != 'all':
        products_query = products_query.filter(Product.category == category)

    if search_query:
        from sqlalchemy import or_
        products_query = products_query.filter(
            or_(
                Product.name.ilike(f'%{search_query}%'),
                Product.brand.ilike(f'%{search_query}%'),
                Product.description.ilike(f'%{search_query}%')
            )
        )

    products = products_query.all()

    top_products = []
    if show_top and not search_query and category == 'all':
        top_products = get_top_selling_products(limit=4, days=30)

    recommendations = []
    if not search_query and category == 'all':
        recommendations = get_recommendations(limit=4)

    return render_template(
        'index.html',
        products=products,
        categories=categories,
        selected_category=category,
        top_products=top_products,
        show_top_section=show_top,
        recommendations=recommendations
    )


@main.route('/my-products')
@login_required
def my_products():

    bought_products = (
        Product.query
        .join(OrderItem, Product.id == OrderItem.product_id)
        .join(OrderItem.order)
        .filter(OrderItem.order.has(user_id=current_user.id))
        .all()
    )

    return render_template('my_products.html', products=bought_products)
