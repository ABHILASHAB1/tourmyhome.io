from typing import Optional
from dataclasses import asdict
from datetime import datetime
from src.core.entities.listing import Listing, ListingStatus
from src.application.interfaces.listing_repository import ListingRepository
from src.application.interfaces.event_publisher import EventPublisher

class UpdateListingUseCase:
    """Use case for updating an existing listing."""
    
    def __init__(self, repo: ListingRepository, publisher: EventPublisher):
        self.repo = repo
        self.publisher = publisher
        
    async def execute(
        self, 
        listing_id: str,
        user_id: str,
        title: Optional[str] = None, 
        description: Optional[str] = None, 
        price_sar: Optional[float] = None, 
        status: Optional[str] = None,
        category_id: Optional[str] = None
    ) -> Listing:
        
        listing = await self.repo.get_by_id(listing_id)
        if not listing:
            raise ValueError("Listing not found")
            
        if listing.seller_id != user_id:
            raise PermissionError("Not authorized to update this listing")
            
        # Apply updates
        if title is not None:
            listing.title = title
        if description is not None:
            listing.description = description
        if price_sar is not None:
            listing.price_sar = price_sar
        if status is not None:
            try:
                listing.status = ListingStatus(status)
            except ValueError:
                raise ValueError(f"Invalid status: {status}")
        if category_id is not None:
            listing.category_id = category_id
            
        listing.updated_at = datetime.utcnow()
        
        # Enforce Domain Rules
        listing.validate()
        
        # Save via abstract port
        updated_listing = await self.repo.update(listing)
        
        # Publish Domain Event
        event_payload = asdict(updated_listing)
        event_payload['created_at'] = event_payload['created_at'].isoformat()
        event_payload['updated_at'] = event_payload['updated_at'].isoformat()
        
        await self.publisher.publish(
            topic="inventory.listing.events",
            event_type="ListingUpdated",
            payload=event_payload
        )
        
        return updated_listing
