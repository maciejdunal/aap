from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import session

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'



def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product_store.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'secret_key'

    db.init_app(app)
    login_manager.init_app(app)
    @app.before_request
    def clear_chat_on_first_request():
        if not session.get("_chat_initialized"):
            session["chat_history"] = []
            session["_chat_initialized"] = True

    from .routes import main
    from .auth_routes import auth
    from .cart_routes import cart
    from .orders_routes import orders
    from .checkout_routes import checkout
    from .my_products_routes import my_products
    from .product_routes import product
    from .reports_routes import reports
    from .chat.routers import chat_bp
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(cart)
    app.register_blueprint(orders)
    app.register_blueprint(checkout)
    app.register_blueprint(my_products)
    app.register_blueprint(product)
    app.register_blueprint(reports)
    app.register_blueprint(chat_bp)

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return db.session.get(User, int(user_id))  # Poprawione dla SQLAlchemy 2.0
