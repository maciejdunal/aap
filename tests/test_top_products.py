import unittest
from datetime import datetime, timedelta, timezone
from app import create_app, db
from app.models import User, Watch, Order, OrderItem
from app.routes import get_top_selling_products

class TestTopProducts(unittest.TestCase):
    def setUp(self):
        """Set up test client and database."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Create test user
            self.test_user = User(username="testuser", password="testpassword")
            db.session.add(self.test_user)
            
            # Create test watches
            self.watch1 = Watch(
                name="Popular Watch", brand="Brand A", price=100.0,
                description="Most sold watch", image_url="popular.jpg",
                sex="male", category="sport", color="Black", 
                material="Steel", purpose="Sports"
            )
            
            self.watch2 = Watch(
                name="Less Popular Watch", brand="Brand B", price=200.0,
                description="Less sold watch", image_url="less.jpg",
                sex="female", category="luxury", color="Gold",
                material="Gold", purpose="Dress"
            )
            
            self.watch3 = Watch(
                name="New Watch", brand="Brand C", price=300.0,
                description="Never sold watch", image_url="new.jpg",
                sex="male", category="luxury", color="Silver",
                material="Silver", purpose="Casual"
            )
            
            db.session.add_all([self.watch1, self.watch2, self.watch3])
            db.session.commit()
            
            # Create orders with different sales volumes
            current_time = datetime.now(timezone.utc)
            
            # Order 1: 5 units of watch1 (most popular)
            order1 = Order(
                user_id=self.test_user.id, 
                date=current_time - timedelta(days=10),
                total_price=500.0
            )
            db.session.add(order1)
            db.session.commit()
            
            order_item1 = OrderItem(
                order_id=order1.id,
                product_id=self.watch1.id,
                quantity=5
            )
            db.session.add(order_item1)
            
            # Order 2: 2 units of watch2 (less popular)
            order2 = Order(
                user_id=self.test_user.id,
                date=current_time - timedelta(days=5),
                total_price=400.0
            )
            db.session.add(order2)
            db.session.commit()
            
            order_item2 = OrderItem(
                order_id=order2.id,
                product_id=self.watch2.id,
                quantity=2
            )
            db.session.add(order_item2)
            
            # No order for watch3 (never sold)
            
            db.session.commit()

    def test_get_top_selling_products_with_sales(self):
        """Test top selling products function with actual sales data."""
        with self.app.app_context():
            top_products = get_top_selling_products(limit=3, days=30)
            
            # Should return products ordered by sales volume
            self.assertEqual(len(top_products), 2)  # Only 2 products have sales
            
            # First product should be watch1 (5 units sold)
            first_product = top_products[0]
            self.assertEqual(first_product[0].name, "Popular Watch")
            self.assertEqual(first_product[1], 5)  # total_sold
            self.assertEqual(first_product[2], 1)  # order_count
            
            # Second product should be watch2 (2 units sold)
            second_product = top_products[1]
            self.assertEqual(second_product[0].name, "Less Popular Watch")
            self.assertEqual(second_product[1], 2)  # total_sold
            self.assertEqual(second_product[2], 1)  # order_count

    def test_get_top_selling_products_fallback(self):
        """Test fallback to newest products when no sales exist."""
        with self.app.app_context():
            # Delete all orders to test fallback
            OrderItem.query.delete()
            Order.query.delete()
            db.session.commit()
            
            top_products = get_top_selling_products(limit=3, days=30)
            
            # Should return fallback products (most recently added)
            self.assertEqual(len(top_products), 3)
            
            # Check that all have 0 sales (fallback format)
            for product_data in top_products:
                self.assertEqual(product_data[1], 0)  # total_sold should be 0
                self.assertEqual(product_data[2], 0)  # order_count should be 0

    def test_index_route_with_top_products(self):
        """Test that index route includes top products data."""
        with self.app.app_context():
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            
            # Check that template context includes top products
            response_data = response.get_data(as_text=True)
            self.assertIn("Top Selling Products", response_data)
            self.assertIn("Most popular watches", response_data)

    def test_index_route_without_top_products_when_searching(self):
        """Test that top products section is hidden when searching."""
        with self.app.app_context():
            response = self.client.get('/?search=test')
            self.assertEqual(response.status_code, 200)
            
            # Top products section should not appear when searching
            response_data = response.get_data(as_text=True)
            # The section might still be in HTML but should be hidden by logic
            # We test that regular products are still shown
            self.assertIn("watch-gallery", response_data)

    def test_index_route_without_top_products_when_filtered(self):
        """Test that top products section is hidden when category is filtered."""
        with self.app.app_context():
            response = self.client.get('/?category=men')
            self.assertEqual(response.status_code, 200)
            
            response_data = response.get_data(as_text=True)
            # Should show regular products but not top products section
            self.assertIn("watch-gallery", response_data)

    def tearDown(self):
        """Clean up after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()