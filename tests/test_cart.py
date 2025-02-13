import unittest
from app import create_app, db
from app.models import User, Watch, CartItem

class TestCart(unittest.TestCase):
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

    def test_add_to_cart(self):
        """Test dodawania produktu do koszyka"""
        with self.app.app_context():
            user = User.query.get(self.user_id)
            watch = Watch.query.get(self.watch_id)

            with self.client.session_transaction() as sess:
                sess['_user_id'] = str(user.id)

            response = self.client.post(f'/cart/add/{watch.id}')
            self.assertEqual(response.status_code, 302)

            cart_items = CartItem.query.filter_by(user_id=user.id).all()
            self.assertEqual(len(cart_items), 1)

    def tearDown(self):
        """Czyszczenie bazy danych po każdym teście"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()
