import unittest
from app import create_app, db
from app.models import User, Watch, CartItem

class TestCart(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            self.user = User(username="testuser", password="testpassword")
            self.watch = Watch(name="Test Watch", brand="Test Brand", price=100.0,
                               description="Test Desc", image_url="test.jpg", sex="male", category="sport",
                               color="Black", material="Steel", purpose="Testing")
            db.session.add(self.user)
            db.session.add(self.watch)
            db.session.commit()
            self.user_id = self.user.id
            self.watch_id = self.watch.id

    def test_add_to_cart(self):
        with self.app.app_context():
            user = db.session.get(User, self.user_id)  # Poprawione
            watch = db.session.get(Watch, self.watch_id)  # Poprawione

            with self.client.session_transaction() as sess:
                sess['_user_id'] = str(user.id)

            response = self.client.post(f'/cart/add/{watch.id}')
            self.assertEqual(response.status_code, 302)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
