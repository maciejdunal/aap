from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import CartItem, Product, ProductClick
from app.recommender.content_based import get_similar_products_for_cart
from flask import session
from app.recommender.bandit import bandit
cart = Blueprint('cart', __name__)

@cart.route('/cart')
@login_required
def view_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total_price = sum(item.quantity * item.product.price for item in cart_items)

    # 🧠 CONTENT-BASED RECOMMENDATIONS (based on cart)
    similar_products = []
    if cart_items:
        similar_products = get_similar_products_for_cart(cart_items, limit=4)

    print("similar_products", similar_products)
    return render_template(
        'cart.html',
        cart_items=cart_items,
        total_price=total_price,
        similar_products=similar_products
    )

@cart.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    try:
        product = Product.query.get_or_404(product_id)

        # ===============================
        # PARSE AI METADATA (SAFE)
        # ===============================
        data = request.get_json(silent=True) or {}
        source = data.get("source", "organic")   # organic / recommendation
        strategy = data.get("strategy")          # collaborative / content_based / popular

        # ===============================
        # TRACK CLICK (BEHAVIOR DATA)
        # ===============================
        try:
            click = ProductClick(
                product_id=product_id,
                user_id=current_user.id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                referrer=request.headers.get('Referer')
            )
            db.session.add(click)
        except Exception as e:
            print(f"Error recording click: {e}")

        # ===============================
        # CART LOGIC
        # ===============================
        existing_item = CartItem.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()

        if existing_item:
            existing_item.quantity += 1
            message = f'{product.name} quantity updated in cart!'
        else:
            new_item = CartItem(
                user_id=current_user.id,
                product_id=product_id,
                quantity=1,
                source_strategy=strategy if source == "recommendation" else None
            )
            db.session.add(new_item)
            message = f'{product.name} added to cart!'

        db.session.commit()

        # ===============================
        # 🎯 REINFORCEMENT LEARNING UPDATE
        # ===============================
        print(source)
        print(strategy)
        if source == "recommendation" and strategy:
            # reward za add_to_cart
            bandit.update(strategy, reward=2)

        # ===============================
        # AJAX RESPONSE
        # ===============================
        if (
            request.headers.get('Content-Type') == 'application/json'
            or request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        ):
            return jsonify({
                'success': True,
                'message': message,
                'product_name': product.name
            })

        flash(message)
        return redirect(url_for('main.index'))

    except Exception as e:
        db.session.rollback()
        error_message = 'Failed to add item to cart. Please try again.'

        if (
            request.headers.get('Content-Type') == 'application/json'
            or request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        ):
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
    cart_item = CartItem.query.filter_by(
        id=item_id,
        user_id=current_user.id
    ).first()

    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        
        # 🧠 Reinforcement Learning penalty: remove from cart
        if cart_item.source_strategy:
            bandit.update(cart_item.source_strategy, reward=-1)

        flash('Item removed from cart.')

    return redirect(url_for('cart.view_cart'))
