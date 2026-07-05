from dataclasses import dataclass
from typing import Optional
from enum import Enum
import uuid
from datetime import datetime

class ListingStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    SOLD = "SOLD"
    FLAGGED = "FLAGGED"

@dataclass
class Listing:
    seller_id: str
    title: str
    description: str
    price_sar: float
    status: ListingStatus
    category_id: Optional[str] = None
    id: str = dataclass.field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = dataclass.field(default_factory=datetime.utcnow)
    updated_at: datetime = dataclass.field(default_factory=datetime.utcnow)

    def validate(self):
        if self.price_sar < 1.0:
            raise ValueError("Price must be at least 1.00 SAR (GBR-002)")
        if len(self.title) > 100:
            raise ValueError("Title cannot exceed 100 characters")
