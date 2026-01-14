from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import Watch, OrderItem, Order, WatchClick, CartItem, db
from sqlalchemy import func, desc
from datetime import datetime, timedelta, timezone

main = Blueprint('main', __name__)

def get_recommendations(limit=4):
    """Get product recommendations based on user's interested brands."""
    interested_brands = set()
    
    # Helper to extract brands
    def extract_brands(query_result):
        return {b[0] for b in query_result}

    if current_user.is_authenticated:
        # Get brands from clicks for logged in user (by User ID)
        user_click_brands = db.session.query(Watch.brand)\
            .join(WatchClick, Watch.id == WatchClick.watch_id)\
            .filter(WatchClick.user_id == current_user.id)\
            .distinct().all()
        interested_brands.update(extract_brands(user_click_brands))
        
        # Get brands from cart for logged in user
        cart_brands = db.session.query(Watch.brand)\
            .join(CartItem, Watch.id == CartItem.product_id)\
            .filter(CartItem.user_id == current_user.id)\
            .distinct().all()
        interested_brands.update(extract_brands(cart_brands))

        # Get brands from past orders for logged in user (Purchase History)
        order_brands = db.session.query(Watch.brand)\
            .join(OrderItem, Watch.id == OrderItem.product_id)\
            .join(Order, OrderItem.order_id == Order.id)\
            .filter(Order.user_id == current_user.id)\
            .distinct().all()
        interested_brands.update(extract_brands(order_brands))
    else:
        ip_address = request.remote_addr
        
        ip_click_brands = db.session.query(Watch.brand)\
            .join(WatchClick, Watch.id == WatchClick.watch_id)\
            .filter(WatchClick.ip_address == ip_address)\
            .distinct().all()
        interested_brands.update(extract_brands(ip_click_brands))
    
    if not interested_brands:
        return []

    # Get products from these brands, Using random ordering to keep it fresh
    recommended = Watch.query.filter(Watch.brand.in_(interested_brands))\
        .order_by(func.random())\
        .limit(limit)\
        .all()
        
    return recommended

@main.route('/api/recommendations-html')
def get_recommendations_html():
    """Get the HTML for the recommendations section."""
    recommendations = get_recommendations(limit=4)
    if not recommendations:
        return '', 204
        
    return render_template('partials/recommendations.html', recommendations=recommendations)

def get_top_selling_products(limit=4, days=30):
    """Get top selling products based on sales in the last N days."""
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    # Query to get top selling products with sales count
    top_products = (
        db.session.query(
            Watch,
            func.sum(OrderItem.quantity).label('total_sold'),
            func.count(OrderItem.id).label('order_count')
        )
        .join(OrderItem, Watch.id == OrderItem.product_id)
        .join(Order, OrderItem.order_id == Order.id)
        .filter(Order.date >= cutoff_date)
        .group_by(Watch.id)
        .order_by(desc('total_sold'))
        .limit(limit)
        .all()
    )
    
    # If no sales in the specified period, return most recently added products
    if not top_products:
        fallback_products = (
            Watch.query
            .order_by(desc(Watch.id))  # Most recently added
            .limit(limit)
            .all()
        )
        # Format as tuples to match the expected structure
        return [(watch, 0, 0) for watch in fallback_products]
    
    return top_products

@main.route('/')
def index():
    category = request.args.get('category', 'all')
    search_query = request.args.get('search', '').strip().lower()
    show_top = request.args.get('show_top', 'true').lower() == 'true'

    # Get top selling products for the main display
    top_products = get_top_selling_products(limit=4, days=30) if show_top and not search_query and category == 'all' else []
    
    # Get regular products based on filters
    if category == 'all':
        watches = Watch.query
    elif category == 'men':
        watches = Watch.query.filter_by(sex='male')
    elif category == 'women':
        watches = Watch.query.filter_by(sex='female')
    elif category == 'luxury':
        watches = Watch.query.filter_by(category='luxury')
    elif category == 'sport':
        watches = Watch.query.filter_by(category='sport')
    else:
        watches = Watch.query

    if search_query:
        watches = watches.filter(Watch.brand.ilike(f'%{search_query}%'))

    watches = watches.all()
    
    # Get recommendations for the initial page load
    recommendations = get_recommendations(limit=4)

    return render_template('index.html', 
                         watches=watches, 
                         top_products=top_products,
                         show_top_section=bool(top_products),
                         recommendations=recommendations)

@main.route('/my-watches')
@login_required
def my_watches():

    bought_watches = (
        Watch.query
        .join(OrderItem, Watch.id == OrderItem.product_id)
        .join(OrderItem.order)
        .filter(OrderItem.order.has(user_id=current_user.id))
        .all()
    )

    return render_template('my_watches.html', watches=bought_watches)
