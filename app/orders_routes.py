from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Order

orders = Blueprint('orders', __name__)

@orders.route('/orders')
@login_required
def view_orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('orders.html', orders=user_orders)
