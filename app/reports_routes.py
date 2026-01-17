from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models import Product, ProductClick, db
from sqlalchemy import func, desc
from datetime import datetime, timedelta, timezone
from app.recommender.bandit import bandit
from flask import session
reports = Blueprint('reports', __name__)

@reports.route('/api/track-click', methods=['POST'])
def track_click():
    """API endpoint to track product clicks."""
    try:
        data = request.get_json()
        
        if not data or 'product_id' not in data:
            return jsonify({'error': 'Product ID is required'}), 400
        
        product_id = data.get('product_id')
        
        product = db.session.get(Product, product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        user_id = None
        try:
            if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
                user_id = current_user.id
        except:
            user_id = None
        
        click = ProductClick(
            product_id=product_id,
            user_id=user_id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            referrer=request.headers.get('Referer')
        )
        
        db.session.add(click)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Click tracked successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@reports.route('/reports')
@login_required
def reports_dashboard():
    """Main reports dashboard showing most clicked products."""

    days = request.args.get('days', 30, type=int)
    if days not in [7, 30, 90, 365]: 
        days = 30
    
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    most_clicked = (
        db.session.query(
            Product,
            func.count(ProductClick.id).label('click_count'),
            func.count(func.distinct(ProductClick.user_id)).label('unique_users'),
            func.count(func.distinct(ProductClick.ip_address)).label('unique_ips')
        )
        .join(ProductClick, Product.id == ProductClick.product_id)
        .filter(ProductClick.timestamp >= cutoff_date)
        .group_by(Product.id)
        .order_by(desc('click_count'))
        .limit(20)
        .all()
    )
    
    total_clicks = (
        ProductClick.query
        .filter(ProductClick.timestamp >= cutoff_date)
        .count()
    )
    
    unique_products_clicked = (
        db.session.query(func.count(func.distinct(ProductClick.product_id)))
        .filter(ProductClick.timestamp >= cutoff_date)
        .scalar()
    )
    
    total_Products = Product.query.count()
    
    daily_trends = get_daily_click_trends(days)
    
    return render_template('reports.html',
                         most_clicked=most_clicked,
                         total_clicks=total_clicks,
                         unique_products_clicked=unique_products_clicked,
                         total_products=total_productes,
                         days=days,
                         daily_trends=daily_trends)

@reports.route('/reports/product/<int:product_id>')
@login_required
def product_details(product_id):
    """Detailed analytics for a specific product."""
    product = db.session.get(Product, product_id)
    if not product:
        return "Product not found", 404
    
    days = request.args.get('days', 30, type=int)
    if days not in [7, 30, 90, 365]:
        days = 30
    
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    # Get click statistics for this product
    clicks = (
        ProductClick.query
        .filter(ProductClick.product_id == product_id)
        .filter(ProductClick.timestamp >= cutoff_date)
        .order_by(desc(ProductClick.timestamp))
        .all()
    )
    
    total_clicks = len(clicks)
    unique_users = len(set(click.user_id for click in clicks if click.user_id))
    unique_ips = len(set(click.ip_address for click in clicks if click.ip_address))
    
    # Get hourly distribution
    hourly_clicks = {}
    for click in clicks:
        hour = click.timestamp.hour
        hourly_clicks[hour] = hourly_clicks.get(hour, 0) + 1
    
    return render_template('product_details.html',
                         product=product,
                         total_clicks=total_clicks,
                         unique_users=unique_users,
                         unique_ips=unique_ips,
                         recent_clicks=clicks[:50],  # Show last 50 clicks
                         hourly_clicks=hourly_clicks,
                         days=days)

def get_daily_click_trends(days):
    """Get daily click counts for trend analysis."""
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    # Query to get clicks grouped by date
    daily_clicks = (
        db.session.query(
            func.date(ProductClick.timestamp).label('date'),
            func.count(ProductClick.id).label('count')
        )
        .filter(ProductClick.timestamp >= cutoff_date)
        .group_by(func.date(ProductClick.timestamp))
        .order_by('date')
        .all()
    )
    
    # Convert to dictionary for easier template usage
    trends = {}
    for date, count in daily_clicks:
        trends[str(date)] = count
    
    return trends

@reports.route('/api/reports/export')
@login_required
def export_reports():
    """Export click data as JSON for external analysis."""
    days = request.args.get('days', 30, type=int)
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    clicks = (
        db.session.query(ProductClick, Product)
        .join(Product, ProductClick.product_id == Product.id)
        .filter(ProductClick.timestamp >= cutoff_date)
        .all()
    )
    
    export_data = []
    for click, product in clicks:
        export_data.append({
            'timestamp': click.timestamp.isoformat(),
            'product_id': product.id,
            'product_name': product.name,
            'product_brand': product.brand,
            'product_price': product.price,
            'product_category': product.category,
            'user_id': click.user_id,
            'ip_address': click.ip_address[:8] + '...' if click.ip_address else None,  # Partial IP for privacy
            'user_agent': click.user_agent[:50] + '...' if click.user_agent and len(click.user_agent) > 50 else click.user_agent
        })
    
    return jsonify({
        'period_days': days,
        'total_records': len(export_data),
        'data': export_data
    })