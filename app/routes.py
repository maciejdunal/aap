from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import Watch, OrderItem

main = Blueprint('main', __name__)

@main.route('/')
def index():
    category = request.args.get('category', 'all')
    search_query = request.args.get('search', '').strip().lower()

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

    return render_template('index.html', watches=watches)

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
