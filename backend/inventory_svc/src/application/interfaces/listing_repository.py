from abc import ABC, abstractmethod
from typing import Optional
from src.core.entities.listing import Listing

class ListingRepository(ABC):
    """Abstract base class (Port) for Listing data access."""
    
    @abstractmethod
    async def create(self, listing: Listing) -> Listing:
        pass
        
    @abstractmethod
    async def get_by_id(self, listing_id: str) -> Optional[Listing]:
        pass
        
    @abstractmethod
    async def update(self, listing: Listing) -> Listing:
        pass
        
    @abstractmethod
    async def delete(self, listing: Listing) -> None:
        pass
