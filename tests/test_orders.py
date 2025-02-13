import unittest
from app import create_app, db
from app.models import User, Order, OrderItem, Watch

class TestOrders(unittest.TestCase):
    def setUp(self):
        """Konfiguracja aplikacji testowej i bazy danych"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            self.create_test_data()

    def create_test_data(self):
        """Tworzenie użytkownika i zegarka dla testów"""
        user = User(username="testuser", password="testpassword")
        watch = Watch(
            name="Test Watch", brand="Test Brand", price=100.0,
            description="Test Desc", image_url="test.jpg",
            sex="male", category="sport"
        )
        db.session.add(user)
        db.session.add(watch)
        db.session.commit()

        self.user_id = user.id
        self.watch_id = watch.id

    def test_create_order(self):
        """Test tworzenia zamówienia"""
        with self.app.app_context():
            user = User.query.get(self.user_id)
            watch = Watch.query.get(self.watch_id)

            order = Order(user_id=user.id, total_price=100.0)
            db.session.add(order)
            db.session.commit()

            order_item = OrderItem(order_id=order.id, product_id=watch.id, quantity=1)
            db.session.add(order_item)
            db.session.commit()

            self.assertEqual(len(Order.query.all()), 1)
            self.assertEqual(len(order.items), 1)

    def tearDown(self):
        """Czyszczenie bazy danych po każdym teście"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()
