from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required
from app.models import Watch, db

product = Blueprint('product', __name__)

@product.route('/products')
@login_required
def list_products():
    """List all products for management."""
    watches = Watch.query.all()
    return render_template('products_list.html', watches=watches)

@product.route('/product/edit/<int:product_id>')
@login_required
def edit_product(product_id):
    """Display edit form for a product."""
    watch = db.session.get(Watch, product_id)
    if watch is None:
        abort(404)
    return render_template('edit_product.html', watch=watch)

@product.route('/product/edit/<int:product_id>', methods=['POST'])
@login_required
def update_product(product_id):
    """Update product details."""
    watch = db.session.get(Watch, product_id)
    if watch is None:
        abort(404)
    
    try:
        # Update basic fields
        watch.name = request.form.get('name', watch.name)
        watch.brand = request.form.get('brand', watch.brand)
        watch.price = float(request.form.get('price', watch.price))
        watch.description = request.form.get('description', watch.description)
        watch.image_url = request.form.get('image_url', watch.image_url)
        watch.sex = request.form.get('sex', watch.sex)
        watch.category = request.form.get('category', watch.category)
        
        # Update new fields
        watch.color = request.form.get('color', watch.color)
        watch.material = request.form.get('material', watch.material)
        watch.purpose = request.form.get('purpose', watch.purpose)
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('product.list_products'))
        
    except ValueError as e:
        flash('Invalid price format. Please enter a valid number.', 'error')
        return redirect(url_for('product.edit_product', product_id=product_id))
    except Exception as e:
        flash('An error occurred while updating the product.', 'error')
        db.session.rollback()
        return redirect(url_for('product.edit_product', product_id=product_id))

@product.route('/product/new')
@login_required
def new_product():
    """Display form for creating a new product."""
    return render_template('new_product.html')

@product.route('/product/new', methods=['POST'])
@login_required
def create_product():
    """Create a new product."""
    try:
        new_watch = Watch(
            name=request.form['name'],
            brand=request.form['brand'],
            price=float(request.form['price']),
            description=request.form['description'],
            image_url=request.form['image_url'],
            sex=request.form['sex'],
            category=request.form['category'],
            color=request.form.get('color'),
            material=request.form.get('material'),
            purpose=request.form.get('purpose')
        )
        
        db.session.add(new_watch)
        db.session.commit()
        flash('Product created successfully!', 'success')
        return redirect(url_for('product.list_products'))
        
    except ValueError as e:
        flash('Invalid price format. Please enter a valid number.', 'error')
        return redirect(url_for('product.new_product'))
    except Exception as e:
        flash('An error occurred while creating the product.', 'error')
        return redirect(url_for('product.new_product'))

@product.route('/product/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    """Delete a product."""
    watch = db.session.get(Watch, product_id)
    if watch is None:
        abort(404)
    
    try:
        db.session.delete(watch)
        db.session.commit()
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        flash('An error occurred while deleting the product.', 'error')
        db.session.rollback()
    
    return redirect(url_for('product.list_products'))