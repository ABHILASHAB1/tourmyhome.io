from database import SessionLocal, engine
import models.listing as models_listing
import models.user as models_user
from core.security import get_password_hash

def seed_marketplace():
    """
    This script generates dummy data directly into the SQLite database.
    It uses highly reliable placeholder URLs instead of the Flickr API.
    """
    print("--- SouqAI KSA Database Seeder (SQLAlchemy) ---")
    
    # 1. Create tables
    models_listing.Base.metadata.create_all(bind=engine)
    models_user.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # 2. Seed Admin User
    if not db.query(models_user.User).filter(models_user.User.email == "admin@souqai.com").first():
        hashed_pw = get_password_hash("password123")
        admin = models_user.User(email="admin@souqai.com", hashed_password=hashed_pw)
        db.add(admin)
        db.commit()
        print("-> Seeded Admin User: admin@souqai.com / password123")

    # 3. Check if already seeded listings
    if db.query(models_listing.Listing).count() > 0:
        print("Database already contains listings. Skipping seed.")
        db.close()
        return

    # 3. Define dummy data
    dummy_data = [
        {
            "title": "2023 Toyota Camry LE - Pristine Condition",
            "description": "Used Toyota Camry, low mileage, excellent for daily commuting in Riyadh.",
            "price_sar": 85000.0,
            "category": "Cars",
            # Unsplash placeholder for a car
            "image_url": "https://images.unsplash.com/photo-1550355291-bbee04a92027?w=800&q=80"
        },
        {
            "title": "Modern 2BHK Apartment in Al Olaya",
            "description": "Spacious fully furnished 2 bedroom apartment. Close to Kingdom Centre.",
            "price_sar": 45000.0,
            "category": "Real Estate",
            # Unsplash placeholder for an apartment interior
            "image_url": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&q=80"
        },
        {
            "title": "iPhone 15 Pro Max - 256GB Titanium",
            "description": "Brand new sealed iPhone 15 Pro Max. Unlocked.",
            "price_sar": 4200.0,
            "category": "Electronics",
            # Unsplash placeholder for a phone
            "image_url": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=800&q=80"
        }
    ]
    
    # 4. Insert into database
    print("Seeding database...")
    for data in dummy_data:
        listing = models_listing.Listing(**data)
        db.add(listing)
        print(f"  -> Inserted: {data['title']}")
        
    db.commit()
    db.close()
    
    print("\n--- Seeding Complete! ---")
    print("Run `uvicorn main:app --reload` to test the API.")

if __name__ == "__main__":
    seed_marketplace()
