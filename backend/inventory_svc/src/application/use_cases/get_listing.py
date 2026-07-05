from typing import Optional
from src.core.entities.listing import Listing
from src.application.interfaces.listing_repository import ListingRepository

class GetListingUseCase:
    """Use case for retrieving a listing by ID."""
    
    def __init__(self, repo: ListingRepository):
        self.repo = repo
        
    async def execute(self, listing_id: str) -> Optional[Listing]:
        return await self.repo.get_by_id(listing_id)
