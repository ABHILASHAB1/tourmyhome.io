from dataclasses import asdict
from src.core.entities.message import Message
from src.infrastructure.web.connection_manager import manager

class SendMessageUseCase:
    """Handles the business logic of sending a message."""
    
    async def execute(self, sender_id: str, recipient_id: str, listing_id: str, content: str) -> dict:
        message = Message(
            sender_id=sender_id,
            recipient_id=recipient_id,
            listing_id=listing_id,
            content=content
        )
        
        # Enforce domain rules
        message.validate()
        
        # Serialize for transport
        payload = asdict(message)
        payload['timestamp'] = payload['timestamp'].isoformat()
        
        # Broadcast the message to the Redis Pub/Sub backplane
        # so any server instance holding the recipient's websocket can deliver it
        await manager.broadcast_to_cluster(payload)
        
        return payload
