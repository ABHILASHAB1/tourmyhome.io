from database import SessionLocal
import models.listing as models
from ai.vector_store import embed_and_upsert

def initialize_vector_db():
    print("--- SouqAI Vector DB Initializer ---")
    
    # Fetch all listings from SQLite
    db = SessionLocal()
    listings = db.query(models.Listing).all()
    db.close()
    
    if not listings:
        print("[!] No listings found in SQLite. Run `python seed.py` first.")
        return
        
    print(f"Found {len(listings)} listings in SQLite. Generating vectors...")
    
    # Push to Qdrant
    embed_and_upsert(listings)
    print("Vector database is now ready for semantic search!")

if __name__ == "__main__":
    initialize_vector_db()
