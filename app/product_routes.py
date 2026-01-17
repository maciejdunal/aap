from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required
from app.models import Product, db

product = Blueprint('product', __name__)

@product.route('/products')
@login_required
def list_products():
    """List all products for management."""
    products = Product.query.all()
    return render_template('products_list.html', products=products)

@product.route('/product/edit/<int:product_id>')
@login_required
def edit_product(product_id):
    """Display edit form for a product."""
    product = db.session.get(Product, product_id)
    if product is None:
        abort(404)
    return render_template('edit_product.html', product=product)

@product.route('/product/edit/<int:product_id>', methods=['POST'])
@login_required
def update_product(product_id):
    """Update product details."""
    product = db.session.get(Products, product_id)
    if product is None:
        abort(404)
    
    try:
        # Update basic fields
        product.name = request.form.get('name', product.name)
        product.brand = request.form.get('brand', product.brand)
        product.price = float(request.form.get('price', product.price))
        product.description = request.form.get('description', product.description)
        product.image_url = request.form.get('image_url', product.image_url)
        product.sex = request.form.get('sex', product.sex)
        product.category = request.form.get('category', product.category)
        
        # Update new fields
        product.color = request.form.get('color', product.color)
        product.material = request.form.get('material', product.material)
        product.purpose = request.form.get('purpose', product.purpose)
        
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
        new_product = Product(
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
        
        db.session.add(new_product)
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
    product = db.session.get(Product, product_id)
    if product is None:
        abort(404)
    
    try:
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        flash('An error occurred while deleting the product.', 'error')
        db.session.rollback()
    
    return redirect(url_for('product.list_products'))