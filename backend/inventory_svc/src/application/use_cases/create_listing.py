from src.core.entities.listing import Listing, ListingStatus
from src.application.interfaces.listing_repository import ListingRepository
from src.application.interfaces.event_publisher import EventPublisher
from dataclasses import asdict

class CreateListingUseCase:
    """Use case for creating a new listing. Enforces business rules."""
    
    def __init__(self, repo: ListingRepository, publisher: EventPublisher):
        self.repo = repo
        self.publisher = publisher
        
    async def execute(self, seller_id: str, title: str, description: str, price_sar: float, category_id: str = None) -> Listing:
        # Create Entity
        listing = Listing(
            seller_id=seller_id,
            title=title,
            description=description,
            price_sar=price_sar,
            status=ListingStatus.ACTIVE,
            category_id=category_id
        )
        
        # Enforce Domain Rules
        listing.validate()
        
        # Save via abstract port
        saved_listing = await self.repo.create(listing)
        
        # Publish Domain Event asynchronously
        # Convert datetime objects to ISO strings for JSON serialization
        event_payload = asdict(saved_listing)
        event_payload['created_at'] = event_payload['created_at'].isoformat()
        event_payload['updated_at'] = event_payload['updated_at'].isoformat()
        
        await self.publisher.publish(
            topic="inventory.listing.events",
            event_type="ListingCreated",
            payload=event_payload
        )
        
        return saved_listing
