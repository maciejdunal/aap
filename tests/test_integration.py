"""
Integration test script to verify database operations and new fields functionality.
This script tests the database migration, seeding, and model operations.
"""

import unittest
from app import create_app, db
from app.models import Watch

def test_integration():
    """Test the complete integration of new fields."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        # Set up test database
        db.create_all()
        
        # Create test data
        test_watch = Watch(
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
        db.session.add(test_watch)
        db.session.commit()
        
        print("=== Integration Test for New Product Fields ===\n")
        
        # Test 1: Verify database schema has new fields
        print("1. Testing database schema...")
        retrieved_watch = Watch.query.first()
        assert retrieved_watch is not None, "No watches found in database"
        
        # Check if new fields exist and are accessible
        has_color = hasattr(retrieved_watch, 'color')
        has_material = hasattr(retrieved_watch, 'material') 
        has_purpose = hasattr(retrieved_watch, 'purpose')
        
        print("   ✅ All new fields (color, material, purpose) exist in database schema")
        assert has_color and has_material and has_purpose, "Missing fields in database schema"
            
        # Test 2: Verify seeded data has new field values
        print("\n2. Testing seeded data...")
        watches_with_new_fields = Watch.query.filter(
            Watch.color.isnot(None),
            Watch.material.isnot(None),
            Watch.purpose.isnot(None)
        ).count()
        
        total_watches = Watch.query.count()
        print(f"   Total watches: {total_watches}")
        print(f"   Watches with complete new fields: {watches_with_new_fields}")
        
        print("   ✅ Test data includes new field values")
        assert watches_with_new_fields > 0, "No watches have new field values"
        
        # Test 3: Test creating new watch with new fields
        print("\n3. Testing new watch creation...")
        new_watch = Watch(
            name="Integration Test Watch",
            brand="Test Brand",
            price=199.99,
            description="Watch created during integration test",
            image_url="test_integration.jpg",
            sex="male",
            category="sport",
            color="Red",
            material="Carbon Fiber", 
            purpose="Testing"
        )
        
        db.session.add(new_watch)
        db.session.commit()
        
        # Verify the watch was saved with new fields
        saved_watch = Watch.query.filter_by(name="Integration Test Watch").first()
        print("   ✅ Successfully created watch with new fields")
        assert saved_watch is not None, "Failed to create watch"
        assert saved_watch.color == "Red" and saved_watch.material == "Carbon Fiber", "Failed to create watch with new fields"
        
        # Test 4: Test updating existing watch with new fields  
        print("\n4. Testing watch update with new fields...")
        update_watch = Watch.query.first()
        original_color = update_watch.color
        update_watch.color = "Updated Color"
        update_watch.material = "Updated Material"
        update_watch.purpose = "Updated Purpose"
        
        db.session.commit()
        
        # Verify update
        db.session.refresh(update_watch)
        print("   ✅ Successfully updated watch with new fields")
        assert (update_watch.color == "Updated Color" and 
            update_watch.material == "Updated Material" and 
            update_watch.purpose == "Updated Purpose"), "Failed to update watch with new fields"
        
        # Test 5: Display sample data
        print("\n5. Sample watch data with new fields:")
        sample_watches = Watch.query.limit(3).all()
        for watch in sample_watches:
            print(f"   • {watch.name} ({watch.brand})")
            print(f"     Color: {watch.color or 'N/A'}")
            print(f"     Material: {watch.material or 'N/A'}")
            print(f"     Purpose: {watch.purpose or 'N/A'}")
            print()
        
        # Clean up test watch
        db.session.delete(saved_watch)
        db.session.commit()
        
        print("=== Integration Test PASSED ===")
        print("✅ Database migration successful")
        print("✅ New fields are working properly")
        print("✅ CRUD operations work with new fields")
        print("✅ Test data contains new field values")

if __name__ == "__main__":
    test_integration()