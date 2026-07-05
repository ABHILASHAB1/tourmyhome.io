from typing import Optional
from sqlalchemy.orm import Session
from src.core.entities.listing import Listing
from src.application.interfaces.listing_repository import ListingRepository
from src.infrastructure.database.models import ListingModel

class SQLAListingRepository(ListingRepository):
    """Concrete implementation of ListingRepository using SQLAlchemy."""
    
    def __init__(self, db_session: Session):
        self.db = db_session
        
    async def create(self, listing: Listing) -> Listing:
        db_listing = ListingModel(
            id=listing.id,
            seller_id=listing.seller_id,
            category_id=listing.category_id,
            title=listing.title,
            description=listing.description,
            price_sar=listing.price_sar,
            status=listing.status,
            created_at=listing.created_at,
            updated_at=listing.updated_at
        )
        self.db.add(db_listing)
        self.db.commit()
        self.db.refresh(db_listing)
        return listing
        
    async def get_by_id(self, listing_id: str) -> Optional[Listing]:
        db_listing = self.db.query(ListingModel).filter(
            ListingModel.id == listing_id,
            ListingModel.status != "DELETED"
        ).first()
        
        if not db_listing:
            return None
            
        return Listing(
            id=db_listing.id,
            seller_id=db_listing.seller_id,
            category_id=db_listing.category_id,
            title=db_listing.title,
            description=db_listing.description,
            price_sar=db_listing.price_sar,
            status=db_listing.status,
            created_at=db_listing.created_at,
            updated_at=db_listing.updated_at
        )
        
    async def update(self, listing: Listing) -> Listing:
        db_listing = self.db.query(ListingModel).filter(ListingModel.id == listing.id).first()
        if db_listing:
            db_listing.title = listing.title
            db_listing.description = listing.description
            db_listing.price_sar = listing.price_sar
            db_listing.status = listing.status
            db_listing.category_id = listing.category_id
            db_listing.updated_at = listing.updated_at
            self.db.commit()
            self.db.refresh(db_listing)
        return listing
        
    async def delete(self, listing: Listing) -> None:
        db_listing = self.db.query(ListingModel).filter(ListingModel.id == listing.id).first()
        if db_listing:
            db_listing.status = "DELETED"
            self.db.commit()
