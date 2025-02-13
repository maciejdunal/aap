from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import OrderItem

my_watches = Blueprint('my_watches', __name__)

@my_watches.route('/my-watches')
@login_required
def view_my_watches():
    purchased_watches = {item.watch for order in current_user.orders for item in order.items}
    return render_template('my_watches.html', watches=purchased_watches)
