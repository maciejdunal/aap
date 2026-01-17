from flask import Blueprint, render_template, request, Response, abort
import xml.etree.ElementTree as ET
from app.models import Order, OrderItem
from flask_login import login_required, current_user
from app import db

orders = Blueprint('orders', __name__)

@orders.route('/orders')
@login_required
def view_orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).all()
    print(current_user.id)
    return render_template('orders.html', orders=user_orders)

@orders.route('/orders/<int:order_id>')
@login_required
def order_details(order_id):
    order = db.session.get(Order, order_id)
    if order is None:
        abort(404)
    return render_template('order_details.html', order=order)

@orders.route('/orders/<int:order_id>/xml')
@login_required
def order_details_xml(order_id):
    order = db.session.get(Order, order_id)
    if order is None:
        abort(404)

    root = ET.Element("order", id=str(order.id), date=str(order.date), total_price=f"{order.total_price:.2f}")
    for item in order.items:
        item_name = item.product.name if item.product else "Unknown Product"
        item_price = f"{item.product.price:.2f}" if item.product else "0.00"
        item_element = ET.SubElement(root, "item", name=item_name, quantity=str(item.quantity), price=item_price)

    xml_data = ET.tostring(root, encoding='utf-8', method='xml')

    return Response(xml_data, mimetype='application/xml', headers={"Content-Disposition": f"attachment; filename=order_{order.id}.xml"})
