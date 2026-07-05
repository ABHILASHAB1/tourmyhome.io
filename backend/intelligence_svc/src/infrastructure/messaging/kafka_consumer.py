import json
import os
import asyncio
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain_openai import OpenAIEmbeddings

class IntelligenceEventConsumer:
    """Consumes events from Kafka in the background."""
    
    def __init__(self):
        self.broker = os.getenv("KAFKA_BROKER", "localhost:9092")
        self.qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        self.topic = "inventory.listing.events"
        self.collection_name = "listings"
        self.consumer = None
        self._running = False
        
        # Initialize Qdrant and Embeddings
        try:
            self.qdrant = QdrantClient(url=self.qdrant_url)
            self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            
            # Ensure collection exists
            if not self.qdrant.collection_exists(self.collection_name):
                self.qdrant.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
                )
                print(f"[*] Created Qdrant collection: {self.collection_name}")
        except Exception as e:
            print(f"Warning: Failed to initialize Qdrant/Embeddings: {e}")
            self.qdrant = None
        
    def start(self):
        """Starts the blocking consumer in a separate thread/executor."""
        self._running = True
        try:
            self.consumer = KafkaConsumer(
                self.topic,
                bootstrap_servers=self.broker,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                group_id="intelligence_group",
                auto_offset_reset="earliest"
            )
            print(f"[*] Intelligence Service listening to Kafka topic: {self.topic}")
            
            for message in self.consumer:
                if not self._running:
                    break
                
                event = message.value
                event_type = event.get("event_type")
                
                if event_type == "ListingCreated":
                    payload = event.get("payload", {})
                    listing_id = payload.get("id")
                    title = payload.get("title", "")
                    desc = payload.get("description", "")
                    price = payload.get("price_sar", 0)
                    
                    print(f"--> [QDRANT INGESTION] Processing new listing: {listing_id} - {title}")
                    
                    if self.qdrant and listing_id:
                        # Formulate semantic text
                        text_to_embed = f"Title: {title}\nDescription: {desc}\nPrice: {price} SAR"
                        
                        # Generate Vector
                        vector = self.embeddings.embed_query(text_to_embed)
                        
                        # Upsert into Qdrant
                        point = PointStruct(
                            id=listing_id, 
                            vector=vector, 
                            payload=payload
                        )
                        self.qdrant.upsert(
                            collection_name=self.collection_name,
                            points=[point]
                        )
                        print(f"    [SUCCESS] Upserted {listing_id} into Qdrant.")
                    
        except Exception as e:
            print(f"Warning: Kafka Consumer failed to start or connect: {e}")
            
    def stop(self):
        """Signals the consumer to stop."""
        self._running = False
        if self.consumer:
            self.consumer.close()
