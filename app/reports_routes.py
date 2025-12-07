from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models import Watch, WatchClick, db
from sqlalchemy import func, desc
from datetime import datetime, timedelta, timezone

reports = Blueprint('reports', __name__)

@reports.route('/api/track-click', methods=['POST'])
def track_click():
    """API endpoint to track watch clicks."""
    try:
        data = request.get_json()
        
        if not data or 'watch_id' not in data:
            return jsonify({'error': 'Watch ID is required'}), 400
        
        watch_id = data.get('watch_id')
        
        # Verify watch exists
        watch = db.session.get(Watch, watch_id)
        if not watch:
            return jsonify({'error': 'Watch not found'}), 404
        
        # Get user ID safely
        user_id = None
        try:
            if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
                user_id = current_user.id
        except:
            # If there's any issue with current_user, just set to None for anonymous
            user_id = None
        
        # Create click record
        click = WatchClick(
            watch_id=watch_id,
            user_id=user_id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            referrer=request.headers.get('Referer')
        )
        
        db.session.add(click)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Click tracked successfully'})
        
    except Exception as e:
        # Log the error and return a generic error response
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@reports.route('/reports')
@login_required
def reports_dashboard():
    """Main reports dashboard showing most clicked watches."""
    
    # Get time period from query parameter (default to 30 days)
    days = request.args.get('days', 30, type=int)
    if days not in [7, 30, 90, 365]:  # Restrict to valid periods
        days = 30
    
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    # Get most clicked watches in the specified period
    most_clicked = (
        db.session.query(
            Watch,
            func.count(WatchClick.id).label('click_count'),
            func.count(func.distinct(WatchClick.user_id)).label('unique_users'),
            func.count(func.distinct(WatchClick.ip_address)).label('unique_ips')
        )
        .join(WatchClick, Watch.id == WatchClick.watch_id)
        .filter(WatchClick.timestamp >= cutoff_date)
        .group_by(Watch.id)
        .order_by(desc('click_count'))
        .limit(20)
        .all()
    )
    
    # Get total statistics
    total_clicks = (
        WatchClick.query
        .filter(WatchClick.timestamp >= cutoff_date)
        .count()
    )
    
    unique_watches_clicked = (
        db.session.query(func.count(func.distinct(WatchClick.watch_id)))
        .filter(WatchClick.timestamp >= cutoff_date)
        .scalar()
    )
    
    total_watches = Watch.query.count()
    
    # Get daily click trends for the chart
    daily_trends = get_daily_click_trends(days)
    
    return render_template('reports.html',
                         most_clicked=most_clicked,
                         total_clicks=total_clicks,
                         unique_watches_clicked=unique_watches_clicked,
                         total_watches=total_watches,
                         days=days,
                         daily_trends=daily_trends)

@reports.route('/reports/watch/<int:watch_id>')
@login_required
def watch_details(watch_id):
    """Detailed analytics for a specific watch."""
    watch = db.session.get(Watch, watch_id)
    if not watch:
        return "Watch not found", 404
    
    days = request.args.get('days', 30, type=int)
    if days not in [7, 30, 90, 365]:
        days = 30
    
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    # Get click statistics for this watch
    clicks = (
        WatchClick.query
        .filter(WatchClick.watch_id == watch_id)
        .filter(WatchClick.timestamp >= cutoff_date)
        .order_by(desc(WatchClick.timestamp))
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
    
    return render_template('watch_details.html',
                         watch=watch,
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
            func.date(WatchClick.timestamp).label('date'),
            func.count(WatchClick.id).label('count')
        )
        .filter(WatchClick.timestamp >= cutoff_date)
        .group_by(func.date(WatchClick.timestamp))
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
        db.session.query(WatchClick, Watch)
        .join(Watch, WatchClick.watch_id == Watch.id)
        .filter(WatchClick.timestamp >= cutoff_date)
        .all()
    )
    
    export_data = []
    for click, watch in clicks:
        export_data.append({
            'timestamp': click.timestamp.isoformat(),
            'watch_id': watch.id,
            'watch_name': watch.name,
            'watch_brand': watch.brand,
            'watch_price': watch.price,
            'watch_category': watch.category,
            'user_id': click.user_id,
            'ip_address': click.ip_address[:8] + '...' if click.ip_address else None,  # Partial IP for privacy
            'user_agent': click.user_agent[:50] + '...' if click.user_agent and len(click.user_agent) > 50 else click.user_agent
        })
    
    return jsonify({
        'period_days': days,
        'total_records': len(export_data),
        'data': export_data
    })