from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Order, OrderItem, db
from datetime import datetime

checkout = Blueprint('checkout', __name__)

@checkout.route('/checkout')
@login_required
def view_checkout():
    return render_template('checkout.html')

@checkout.route('/checkout', methods=['POST'])
@login_required
def process_checkout():
    full_name = request.form.get("full_name")
    email = request.form.get("email")
    address = request.form.get("address")
    payment_method = request.form.get("payment_method")

    if not full_name or not email or not address or not payment_method:
        flash("All fields are required!", "danger")
        return redirect(url_for('checkout.view_checkout'))

    new_order = Order(user_id=current_user.id, date=datetime.now(), total_price=0)
    db.session.add(new_order)
    db.session.commit()

    cart_items = current_user.cart_items
    total_price = 0

    for item in cart_items:
        order_item = OrderItem(order_id=new_order.id, product_id=item.product_id, quantity=item.quantity)


        db.session.add(order_item)
        total_price += item.quantity * item.watch.price

    new_order.total_price = total_price
    db.session.commit()

    for item in cart_items:
        db.session.delete(item)

    db.session.commit()

    flash("Order placed successfully!", "success")
    return redirect(url_for('orders.view_orders'))
