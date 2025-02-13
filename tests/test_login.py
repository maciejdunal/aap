import unittest
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

class TestLogin(unittest.TestCase):
    def setUp(self):
        """Konfiguracja aplikacji testowej i bazy danych"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            self.create_test_user()

    def create_test_user(self):
        """Tworzenie testowego użytkownika"""
        user = User(username="testuser", password=generate_password_hash("testpassword"))
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

    def test_login_user(self):
        """Test poprawnego logowania użytkownika"""
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow_redirects=True)

        self.assertIn(b"Logout", response.data)

    def test_login_invalid_user(self):
        """Test logowania nieistniejącego użytkownika"""
        response = self.client.post('/login', data={
            'username': 'wronguser',
            'password': 'wrongpassword'
        }, follow_redirects=True)

        self.assertNotIn(b"Logout", response.data)

    def tearDown(self):
        """Czyszczenie bazy danych po każdym teście"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()
