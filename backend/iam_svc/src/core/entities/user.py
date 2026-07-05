from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import uuid
from datetime import datetime

class UserRole(str, Enum):
    BUYER = "BUYER"
    SELLER = "SELLER"
    ADMIN = "ADMIN"

@dataclass
class User:
    email: str
    hashed_password: str
    role: UserRole = UserRole.BUYER
    nafath_verified: bool = False
    trust_score: int = 100
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)

    def validate(self):
        if "@" not in self.email:
            raise ValueError("Invalid email format")
        if self.trust_score < 0 or self.trust_score > 100:
            raise ValueError("Trust score must be between 0 and 100")
