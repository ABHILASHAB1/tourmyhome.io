from abc import ABC, abstractmethod
from typing import Dict, Any

class EventPublisher(ABC):
    """Abstract base class (Port) for publishing domain events."""
    
    @abstractmethod
    async def publish(self, topic: str, event_type: str, payload: Dict[str, Any]) -> None:
        """Publishes an event to the message broker."""
        pass
