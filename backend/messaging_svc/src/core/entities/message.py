from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class Message:
    sender_id: str
    recipient_id: str
    content: str
    listing_id: str  # The property they are discussing
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def validate(self):
        if not self.content or len(self.content.strip()) == 0:
            raise ValueError("Message content cannot be empty")
        if len(self.content) > 2000:
            raise ValueError("Message content exceeds 2000 characters")
