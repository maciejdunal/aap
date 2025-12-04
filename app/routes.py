from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import Watch, OrderItem, Order, db
from sqlalchemy import func, desc
from datetime import datetime, timedelta, timezone

main = Blueprint('main', __name__)

def get_top_selling_products(limit=5, days=30):
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
    top_products = get_top_selling_products(limit=6, days=30) if show_top and not search_query and category == 'all' else []
    
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

    return render_template('index.html', 
                         watches=watches, 
                         top_products=top_products,
                         show_top_section=bool(top_products))

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
