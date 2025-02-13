import unittest
from app import create_app, db
from app.models import User

class TestRegister(unittest.TestCase):
    def setUp(self):
        """ Konfiguracja aplikacji testowej i bazy danych """
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def test_register_user(self):
        """ Test poprawnej rejestracji użytkownika """
        response = self.client.post('/register', data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)

        with self.app.app_context():
            user = User.query.filter_by(username="testuser").first()
            self.assertIsNotNone(user)

    def tearDown(self):
        """ Czyszczenie bazy danych po każdym teście """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
