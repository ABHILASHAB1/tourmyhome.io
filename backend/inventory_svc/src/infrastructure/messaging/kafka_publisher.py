import json
import os
import asyncio
from kafka import KafkaProducer
from typing import Dict, Any
from src.application.interfaces.event_publisher import EventPublisher

class KafkaEventPublisher(EventPublisher):
    """Concrete implementation of EventPublisher using Apache Kafka."""
    
    def __init__(self):
        broker = os.getenv("KAFKA_BROKER", "localhost:9092")
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=broker,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
        except Exception as e:
            print(f"Warning: Could not connect to Kafka broker {broker}: {e}")
            self.producer = None
            
    async def publish(self, topic: str, event_type: str, payload: Dict[str, Any]) -> None:
        if not self.producer:
            print(f"Mock Publish -> [{topic}] {event_type}: {payload}")
            return
            
        message = {
            "event_type": event_type,
            "payload": payload
        }
        
        # KafkaProducer.send is synchronous, but we can run it in a threadpool to not block asyncio
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.producer.send, topic, message)
        self.producer.flush()
