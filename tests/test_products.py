import unittest
import json
from app import create_app, db
from app.models import User, Watch

class TestProductRoutes(unittest.TestCase):
    def setUp(self):
        """Set up test client and database."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Create test user
            self.test_user = User(username="testuser", password="testpassword")
            db.session.add(self.test_user)
            
            # Create test watches with new fields
            self.test_watch = Watch(
                name="Test Watch", 
                brand="Test Brand", 
                price=100.0,
                description="Test Description", 
                image_url="test.jpg", 
                sex="male", 
                category="sport",
                color="Black",
                material="Stainless Steel",
                purpose="Sports"
            )
            
            self.test_watch_2 = Watch(
                name="Test Watch 2", 
                brand="Test Brand 2", 
                price=200.0,
                description="Test Description 2", 
                image_url="test2.jpg", 
                sex="female", 
                category="luxury",
                color="Rose Gold",
                material="Leather",
                purpose="Dress"
            )
            
            db.session.add(self.test_watch)
            db.session.add(self.test_watch_2)
            db.session.commit()
            
            self.user_id = self.test_user.id
            self.watch_id = self.test_watch.id
            self.watch_id_2 = self.test_watch_2.id

    def login_user(self):
        """Helper method to log in a test user."""
        with self.client.session_transaction() as sess:
            sess['_user_id'] = str(self.user_id)

    def test_list_products_requires_login(self):
        """Test that product list requires authentication."""
        response = self.client.get('/products')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_list_products_authenticated(self):
        """Test product list with authenticated user."""
        self.login_user()
        response = self.client.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Watch', response.data)
        self.assertIn(b'Test Watch 2', response.data)

    def test_edit_product_get_requires_login(self):
        """Test that edit product GET requires authentication."""
        response = self.client.get(f'/product/edit/{self.watch_id}')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_edit_product_get_authenticated(self):
        """Test edit product GET with authenticated user."""
        self.login_user()
        response = self.client.get(f'/product/edit/{self.watch_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Watch', response.data)
        self.assertIn(b'Black', response.data)  # Check new color field
        self.assertIn(b'Stainless Steel', response.data)  # Check new material field
        self.assertIn(b'Sports', response.data)  # Check new purpose field

    def test_edit_product_post_update(self):
        """Test updating a product via POST request."""
        self.login_user()
        
        update_data = {
            'name': 'Updated Test Watch',
            'brand': 'Updated Brand',
            'price': 150.0,
            'description': 'Updated description',
            'image_url': 'updated.jpg',
            'sex': 'female',
            'category': 'luxury',
            'color': 'Blue',
            'material': 'Titanium',
            'purpose': 'Casual'
        }
        
        response = self.client.post(f'/product/edit/{self.watch_id}', data=update_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        
        # Verify the watch was updated
        with self.app.app_context():
            updated_watch = db.session.get(Watch, self.watch_id)
            self.assertEqual(updated_watch.name, 'Updated Test Watch')
            self.assertEqual(updated_watch.brand, 'Updated Brand')
            self.assertEqual(updated_watch.price, 150.0)
            self.assertEqual(updated_watch.color, 'Blue')
            self.assertEqual(updated_watch.material, 'Titanium')
            self.assertEqual(updated_watch.purpose, 'Casual')

    def test_edit_product_invalid_price(self):
        """Test updating product with invalid price."""
        self.login_user()
        
        update_data = {
            'name': 'Updated Test Watch',
            'brand': 'Updated Brand',
            'price': 'invalid_price',  # Invalid price
            'description': 'Updated description',
            'image_url': 'updated.jpg',
            'sex': 'female',
            'category': 'luxury',
            'color': 'Blue',
            'material': 'Titanium',
            'purpose': 'Casual'
        }
        
        response = self.client.post(f'/product/edit/{self.watch_id}', data=update_data)
        self.assertEqual(response.status_code, 302)  # Redirect back to edit page
        
        # Verify the watch was not updated
        with self.app.app_context():
            watch = db.session.get(Watch, self.watch_id)
            self.assertEqual(watch.name, 'Test Watch')  # Should remain unchanged
            self.assertEqual(watch.price, 100.0)  # Should remain unchanged

    def test_new_product_get_requires_login(self):
        """Test that new product GET requires authentication."""
        response = self.client.get('/product/new')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_new_product_get_authenticated(self):
        """Test new product GET with authenticated user."""
        self.login_user()
        response = self.client.get('/product/new')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add New Product', response.data)

    def test_create_new_product(self):
        """Test creating a new product."""
        self.login_user()
        
        new_product_data = {
            'name': 'New Test Watch',
            'brand': 'New Brand',
            'price': 300.0,
            'description': 'New product description',
            'image_url': 'new.jpg',
            'sex': 'male',
            'category': 'sport',
            'color': 'Green',
            'material': 'Carbon Fiber',
            'purpose': 'Running'
        }
        
        response = self.client.post('/product/new', data=new_product_data)
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        
        # Verify the product was created
        with self.app.app_context():
            new_watch = Watch.query.filter_by(name='New Test Watch').first()
            self.assertIsNotNone(new_watch)
            self.assertEqual(new_watch.brand, 'New Brand')
            self.assertEqual(new_watch.price, 300.0)
            self.assertEqual(new_watch.color, 'Green')
            self.assertEqual(new_watch.material, 'Carbon Fiber')
            self.assertEqual(new_watch.purpose, 'Running')

    def test_create_product_missing_required_fields(self):
        """Test creating product with missing required fields."""
        self.login_user()
        
        incomplete_data = {
            'name': 'Incomplete Watch',
            # Missing required fields: brand, price, description, etc.
        }
        
        response = self.client.post('/product/new', data=incomplete_data)
        self.assertEqual(response.status_code, 302)  # Redirect back to form
        
        # Verify no product was created
        with self.app.app_context():
            incomplete_watch = Watch.query.filter_by(name='Incomplete Watch').first()
            self.assertIsNone(incomplete_watch)

    def test_delete_product_requires_login(self):
        """Test that delete product requires authentication."""
        response = self.client.post(f'/product/delete/{self.watch_id}')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_delete_product_authenticated(self):
        """Test deleting a product with authenticated user."""
        self.login_user()
        
        response = self.client.post(f'/product/delete/{self.watch_id}')
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        
        # Verify the product was deleted
        with self.app.app_context():
            deleted_watch = db.session.get(Watch, self.watch_id)
            self.assertIsNone(deleted_watch)

    def test_edit_nonexistent_product(self):
        """Test editing a product that doesn't exist."""
        self.login_user()
        
        response = self.client.get('/product/edit/99999')
        self.assertEqual(response.status_code, 404)  # Not found

    def test_delete_nonexistent_product(self):
        """Test deleting a product that doesn't exist."""
        self.login_user()
        
        response = self.client.post('/product/delete/99999')
        self.assertEqual(response.status_code, 404)  # Not found

    def test_product_model_new_fields(self):
        """Test that the product model correctly handles new fields."""
        with self.app.app_context():
            # Test creating watch with new fields
            watch = Watch(
                name="Field Test Watch",
                brand="Field Brand",
                price=99.99,
                description="Testing new fields",
                image_url="field_test.jpg",
                sex="male",
                category="sport",
                color="Red",
                material="Rubber",
                purpose="Fitness"
            )
            
            db.session.add(watch)
            db.session.commit()
            
            # Retrieve and verify
            saved_watch = Watch.query.filter_by(name="Field Test Watch").first()
            self.assertIsNotNone(saved_watch)
            self.assertEqual(saved_watch.color, "Red")
            self.assertEqual(saved_watch.material, "Rubber")
            self.assertEqual(saved_watch.purpose, "Fitness")

    def test_product_model_nullable_new_fields(self):
        """Test that new fields are nullable."""
        with self.app.app_context():
            # Test creating watch without new fields
            watch = Watch(
                name="Minimal Watch",
                brand="Minimal Brand",
                price=50.0,
                description="Minimal description",
                image_url="minimal.jpg",
                sex="female",
                category="luxury"
                # color, material, purpose not specified
            )
            
            db.session.add(watch)
            db.session.commit()
            
            # Retrieve and verify nulls are handled
            saved_watch = Watch.query.filter_by(name="Minimal Watch").first()
            self.assertIsNotNone(saved_watch)
            self.assertIsNone(saved_watch.color)
            self.assertIsNone(saved_watch.material)
            self.assertIsNone(saved_watch.purpose)

    def tearDown(self):
        """Clean up after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()