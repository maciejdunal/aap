import unittest
import json
from datetime import datetime, timedelta, timezone
from app import create_app, db
from app.models import User, Watch, WatchClick

class TestClickTracking(unittest.TestCase):
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
                name="Clickable Watch", brand="Brand A", price=100.0,
                description="Most clicked watch", image_url="click1.jpg",
                sex="male", category="sport", color="Black", 
                material="Steel", purpose="Sports"
            )
            
            self.watch2 = Watch(
                name="Less Clicked Watch", brand="Brand B", price=200.0,
                description="Less clicked watch", image_url="click2.jpg",
                sex="female", category="luxury", color="Gold",
                material="Gold", purpose="Dress"
            )
            
            db.session.add_all([self.watch1, self.watch2])
            db.session.commit()
            
            self.user_id = self.test_user.id
            self.watch1_id = self.watch1.id
            self.watch2_id = self.watch2.id

    def test_track_click_api_authenticated(self):
        """Test click tracking API with authenticated user."""
        with self.app.app_context():
            # Login user
            with self.client.session_transaction() as sess:
                sess['_user_id'] = str(self.user_id)
            
            # Track a click
            response = self.client.post('/api/track-click',
                                     json={'watch_id': self.watch1_id},
                                     headers={'Content-Type': 'application/json'})
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            
            # Verify click was recorded
            click = WatchClick.query.filter_by(watch_id=self.watch1_id, user_id=self.user_id).first()
            self.assertIsNotNone(click)
            self.assertEqual(click.watch_id, self.watch1_id)
            self.assertEqual(click.user_id, self.user_id)

    def test_track_click_api_anonymous(self):
        """Test click tracking API with anonymous user."""
        with self.app.app_context():
            # Track a click without authentication
            response = self.client.post('/api/track-click',
                                     json={'watch_id': self.watch1_id},
                                     headers={'Content-Type': 'application/json'})
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            
            # Verify click was recorded with no user_id
            click = WatchClick.query.filter_by(watch_id=self.watch1_id, user_id=None).first()
            self.assertIsNotNone(click)
            self.assertEqual(click.watch_id, self.watch1_id)
            self.assertIsNone(click.user_id)

    def test_track_click_invalid_watch(self):
        """Test click tracking with invalid watch ID."""
        with self.app.app_context():
            response = self.client.post('/api/track-click',
                                     json={'watch_id': 99999},
                                     headers={'Content-Type': 'application/json'})
            
            self.assertEqual(response.status_code, 404)
            data = json.loads(response.data)
            self.assertIn('error', data)

    def test_track_click_missing_watch_id(self):
        """Test click tracking without watch ID."""
        with self.app.app_context():
            response = self.client.post('/api/track-click',
                                     json={},
                                     headers={'Content-Type': 'application/json'})
            
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            self.assertIn('error', data)

    def test_reports_dashboard_requires_login(self):
        """Test that reports dashboard requires authentication."""
        response = self.client.get('/reports')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_reports_dashboard_with_data(self):
        """Test reports dashboard with click data."""
        with self.app.app_context():
            # Login user
            with self.client.session_transaction() as sess:
                sess['_user_id'] = str(self.user_id)
            
            # Add some click data
            current_time = datetime.now(timezone.utc)
            
            # 5 clicks for watch1
            for i in range(5):
                click = WatchClick(
                    watch_id=self.watch1_id,
                    user_id=self.user_id,
                    timestamp=current_time - timedelta(hours=i),
                    ip_address='127.0.0.1'
                )
                db.session.add(click)
            
            # 2 clicks for watch2
            for i in range(2):
                click = WatchClick(
                    watch_id=self.watch2_id,
                    user_id=None,  # Anonymous clicks
                    timestamp=current_time - timedelta(hours=i),
                    ip_address='192.168.1.1'
                )
                db.session.add(click)
            
            db.session.commit()
            
            # Test reports dashboard
            response = self.client.get('/reports')
            self.assertEqual(response.status_code, 200)
            
            # Check that response contains expected data
            response_data = response.get_data(as_text=True)
            self.assertIn('Analytics Reports', response_data)
            self.assertIn('Most Clicked Watches', response_data)
            self.assertIn('Clickable Watch', response_data)  # Should appear first (more clicks)
            self.assertIn('Less Clicked Watch', response_data)

    def test_watch_details_page(self):
        """Test individual watch details analytics page."""
        with self.app.app_context():
            # Login user
            with self.client.session_transaction() as sess:
                sess['_user_id'] = str(self.user_id)
            
            # Add click data for specific watch
            current_time = datetime.now(timezone.utc)
            for i in range(3):
                click = WatchClick(
                    watch_id=self.watch1_id,
                    user_id=self.user_id if i < 2 else None,  # Mix of auth/anon
                    timestamp=current_time - timedelta(hours=i),
                    ip_address='127.0.0.1' if i < 2 else '192.168.1.1'
                )
                db.session.add(click)
            
            db.session.commit()
            
            # Test watch details page
            response = self.client.get(f'/reports/watch/{self.watch1_id}')
            self.assertEqual(response.status_code, 200)
            
            response_data = response.get_data(as_text=True)
            self.assertIn('Clickable Watch', response_data)
            self.assertIn('Analytics', response_data)
            self.assertIn('Total Clicks', response_data)

    def test_reports_time_periods(self):
        """Test reports with different time periods."""
        with self.app.app_context():
            # Login user
            with self.client.session_transaction() as sess:
                sess['_user_id'] = str(self.user_id)
            
            # Add clicks from different time periods
            current_time = datetime.now(timezone.utc)
            
            # Recent click (within 7 days)
            recent_click = WatchClick(
                watch_id=self.watch1_id,
                timestamp=current_time - timedelta(days=3)
            )
            db.session.add(recent_click)
            
            # Old click (older than 30 days)
            old_click = WatchClick(
                watch_id=self.watch2_id,
                timestamp=current_time - timedelta(days=45)
            )
            db.session.add(old_click)
            
            db.session.commit()
            
            # Test 7-day period (should show only recent click)
            response = self.client.get('/reports?days=7')
            self.assertEqual(response.status_code, 200)
            response_data = response.get_data(as_text=True)
            self.assertIn('Clickable Watch', response_data)
            
            # Test 90-day period (should show both clicks)
            response = self.client.get('/reports?days=90')
            self.assertEqual(response.status_code, 200)
            response_data = response.get_data(as_text=True)
            self.assertIn('Clickable Watch', response_data)

    def test_export_reports_api(self):
        """Test reports export API."""
        with self.app.app_context():
            # Login user
            with self.client.session_transaction() as sess:
                sess['_user_id'] = str(self.user_id)
            
            # Add some click data
            click = WatchClick(
                watch_id=self.watch1_id,
                user_id=self.user_id,
                ip_address='127.0.0.1',
                user_agent='Test Browser'
            )
            db.session.add(click)
            db.session.commit()
            
            # Test export
            response = self.client.get('/api/reports/export')
            self.assertEqual(response.status_code, 200)
            
            data = json.loads(response.data)
            self.assertIn('data', data)
            self.assertIn('period_days', data)
            self.assertEqual(data['period_days'], 30)  # Default period
            self.assertEqual(data['total_records'], 1)
            
            # Check that export data contains expected fields
            export_record = data['data'][0]
            self.assertEqual(export_record['watch_name'], 'Clickable Watch')
            self.assertEqual(export_record['watch_brand'], 'Brand A')
            self.assertEqual(export_record['user_id'], self.user_id)

    def tearDown(self):
        """Clean up after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()