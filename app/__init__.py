from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///watch_store.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'secret_key'

    db.init_app(app)
    login_manager.init_app(app)


    from .routes import main
    from .auth_routes import auth
    from .cart_routes import cart
    from .orders_routes import orders
    from .checkout_routes import checkout


    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(cart)
    app.register_blueprint(orders)
    app.register_blueprint(checkout)
    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))
