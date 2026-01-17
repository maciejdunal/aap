from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import OrderItem

my_products = Blueprint('my_products', __name__)

@my_products.route('/my_products')
@login_required
def view_my_products():
    purchased_products = {item.product for order in current_user.orders for item in order.items}
    return render_template('my_products.html', products=purchased_products)
