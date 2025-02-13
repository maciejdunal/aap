from flask import Blueprint, render_template, request, Response
import xml.etree.ElementTree as ET
from app.models import Order, OrderItem
from flask_login import login_required, current_user

orders = Blueprint('orders', __name__)

@orders.route('/orders')
@login_required
def view_orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('orders.html', orders=user_orders)

@orders.route('/orders/<int:order_id>')
@login_required
def order_details(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_details.html', order=order)

@orders.route('/orders/<int:order_id>/xml')
@login_required
def order_details_xml(order_id):
    order = Order.query.get_or_404(order_id)

    root = ET.Element("order", id=str(order.id), date=str(order.date), total_price=f"{order.total_price:.2f}")
    for item in order.items:
        item_name = item.watch.name if item.watch else "Unknown Product"
        item_price = f"{item.watch.price:.2f}" if item.watch else "0.00"
        item_element = ET.SubElement(root, "item", name=item_name, quantity=str(item.quantity), price=item_price)

    xml_data = ET.tostring(root, encoding='utf-8', method='xml')

    return Response(xml_data, mimetype='application/xml', headers={"Content-Disposition": f"attachment; filename=order_{order.id}.xml"})
