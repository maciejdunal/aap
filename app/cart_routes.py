from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import CartItem, Watch, WatchClick

cart = Blueprint('cart', __name__)

@cart.route('/cart')
@login_required
def view_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total_price = sum(item.quantity * item.watch.price for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@cart.route('/cart/add/<int:watch_id>', methods=['POST'])
@login_required
def add_to_cart(watch_id):
    try:
        watch = Watch.query.get_or_404(watch_id)
        
        # Record interaction for recommendations (persistent history)
        try:
            click = WatchClick(
                watch_id=watch_id,
                user_id=current_user.id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                referrer=request.headers.get('Referer')
            )
            db.session.add(click)
        except Exception as e:
            print(f"Error recording click in add_to_cart: {e}")

        existing_item = CartItem.query.filter_by(user_id=current_user.id, product_id=watch_id).first()
        
        if existing_item:
            existing_item.quantity += 1
            message = f'{watch.name} quantity updated in cart!'
        else:
            new_item = CartItem(user_id=current_user.id, product_id=watch_id, quantity=1)
            db.session.add(new_item)
            message = f'{watch.name} added to cart!'
        
        db.session.commit()
        
        # Check if this is an AJAX request
        if request.headers.get('Content-Type') == 'application/json' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'message': message,
                'watch_name': watch.name
            })
        
        # Fallback for non-AJAX requests
        flash(message)
        return redirect(url_for('main.index'))
    
    except Exception as e:
        error_message = 'Failed to add item to cart. Please try again.'
        if request.headers.get('Content-Type') == 'application/json' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': False,
                'message': error_message
            }), 400
        
        flash(error_message, 'error')
        return redirect(url_for('main.index'))

@cart.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_quantity(item_id):
    new_quantity = request.form.get('quantity', type=int)
    cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    if cart_item:
        if new_quantity <= 0:
            db.session.delete(cart_item)
            flash('Item removed from cart.')
        else:
            cart_item.quantity = new_quantity
            flash('Quantity updated.')
        db.session.commit()
    return redirect(url_for('cart.view_cart'))

@cart.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_item(item_id):
    cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart.')
    return redirect(url_for('cart.view_cart'))
