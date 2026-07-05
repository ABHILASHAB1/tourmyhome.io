from src.application.interfaces.listing_repository import ListingRepository
from src.application.interfaces.event_publisher import EventPublisher

class DeleteListingUseCase:
    """Use case for soft-deleting a listing."""
    
    def __init__(self, repo: ListingRepository, publisher: EventPublisher):
        self.repo = repo
        self.publisher = publisher
        
    async def execute(self, listing_id: str, user_id: str) -> None:
        listing = await self.repo.get_by_id(listing_id)
        if not listing:
            raise ValueError("Listing not found")
            
        if listing.seller_id != user_id:
            raise PermissionError("Not authorized to delete this listing")
            
        # Soft Delete via abstract port
        await self.repo.delete(listing)
        
        # Publish Domain Event
        await self.publisher.publish(
            topic="inventory.listing.events",
            event_type="ListingDeleted",
            payload={"id": listing.id}
        )
