import os
import json
import asyncio
import redis.asyncio as redis
from fastapi import WebSocket

class ConnectionManager:
    """Manages WebSocket connections and routes messages via Redis Pub/Sub."""
    
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.redis = redis.from_url(self.redis_url)
        self.pubsub = self.redis.pubsub()
        self.channel_name = "chat_messages"
        
        # Start the background listener for Redis Pub/Sub
        asyncio.create_task(self._listen_to_redis())

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"[*] WebSocket connected for user: {user_id}")

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            print(f"[*] WebSocket disconnected for user: {user_id}")

    async def broadcast_to_cluster(self, payload: dict):
        """Publishes the message to the Redis backplane."""
        message_str = json.dumps(payload)
        await self.redis.publish(self.channel_name, message_str)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def _listen_to_redis(self):
        """Background task that listens for messages from Redis and routes them to local WebSockets."""
        await self.pubsub.subscribe(self.channel_name)
        print(f"[*] ConnectionManager subscribed to Redis channel: {self.channel_name}")
        
        try:
            async for message in self.pubsub.listen():
                if message["type"] == "message":
                    data = json.loads(message["data"])
                    recipient_id = data.get("recipient_id")
                    
                    # If the recipient is connected to this specific server instance, push it down the socket
                    if recipient_id in self.active_connections:
                        ws = self.active_connections[recipient_id]
                        try:
                            await ws.send_json(data)
                        except Exception as e:
                            print(f"Failed to send to {recipient_id}: {e}")
                            self.disconnect(recipient_id)
        except Exception as e:
            print(f"Warning: Redis PubSub listener crashed: {e}")

# Global singleton
manager = ConnectionManager()
