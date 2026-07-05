from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

# 1. Initialize local embedding model (no API key required!)
# all-MiniLM-L6-v2 produces 384-dimensional vectors very quickly on CPU
encoder = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Initialize Qdrant Client lazily to avoid multi-process lock issues with Uvicorn --reload
client = None

def get_client():
    global client
    if client is None:
        client = QdrantClient(path="./qdrant_data")
    return client

COLLECTION_NAME = "souqai_listings"

def init_collection():
    """Create the Qdrant collection if it doesn't exist."""
    c = get_client()
    if not c.collection_exists(COLLECTION_NAME):
        c.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        print(f"Created Qdrant collection: {COLLECTION_NAME}")

def embed_and_upsert(listings):
    """Generate vectors for listings and push them into Qdrant."""
    init_collection()
    
    points = []
    for lst in listings:
        # Create a rich string representation for embedding
        text_to_embed = f"{lst.title}. {lst.description}. Category: {lst.category}. Price: {lst.price_sar} SAR."
        vector = encoder.encode(text_to_embed).tolist()
        
        points.append(
            PointStruct(
                id=lst.id,
                vector=vector,
                payload={
                    "title": lst.title,
                    "price_sar": lst.price_sar,
                    "category": lst.category,
                    "image_url": lst.image_url
                }
            )
        )
        
    c = get_client()
    c.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
    print(f"Upserted {len(points)} listings into Qdrant.")

def search_similar(query: str, limit: int = 3):
    """Embed the user's query and search Qdrant for similar listings."""
    init_collection()
    query_vector = encoder.encode(query).tolist()
    
    c = get_client()
    search_result = c.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=limit
    )
    return search_result
