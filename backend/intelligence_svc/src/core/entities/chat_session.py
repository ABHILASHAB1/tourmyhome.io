from dataclasses import dataclass, field
from typing import List, Dict, Optional
import uuid
from datetime import datetime

@dataclass
class ChatSession:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = "anonymous"
    messages: List[Dict[str, str]] = field(default_factory=list)
    user_intent: str = "unknown"
    extracted_filters: Dict[str, str] = field(default_factory=dict)
    retrieved_listings: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def add_message(self, role: str, content: str):
        if role not in ["user", "assistant", "system", "tool"]:
            raise ValueError(f"Invalid role: {role}")
        self.messages.append({"role": role, "content": content})
        self.updated_at = datetime.utcnow()
