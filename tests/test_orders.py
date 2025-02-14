import unittest
from app import create_app, db
from app.models import User, Order, OrderItem, Watch

class TestOrders(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            self.user = User(username="testuser", password="testpassword")
            self.watch = Watch(name="Test Watch", brand="Test Brand", price=100.0,
                               description="Test Desc", image_url="test.jpg", sex="male", category="sport")
            db.session.add(self.user)
            db.session.add(self.watch)
            db.session.commit()
            self.user_id = self.user.id
            self.watch_id = self.watch.id

    def test_create_order(self):
        with self.app.app_context():
            user = db.session.get(User, self.user_id)  # Poprawione
            watch = db.session.get(Watch, self.watch_id)  # Poprawione

            with self.client.session_transaction() as sess:
                sess['_user_id'] = str(user.id)

            order = Order(user_id=user.id, total_price=100.0)
            db.session.add(order)
            db.session.commit()

            order_item = OrderItem(order_id=order.id, product_id=watch.id, quantity=1)
            db.session.add(order_item)
            db.session.commit()

            self.assertEqual(len(Order.query.all()), 1)
            self.assertEqual(len(order.items), 1)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
