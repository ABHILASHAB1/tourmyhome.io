from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
from src.infrastructure.web.routers import chat_router
from src.infrastructure.messaging.kafka_consumer import IntelligenceEventConsumer

consumer = IntelligenceEventConsumer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Run the blocking Kafka consumer in a background thread
    loop = asyncio.get_event_loop()
    task = loop.run_in_executor(None, consumer.start)
    yield
    # Shutdown: Stop the consumer
    consumer.stop()
    await task

app = FastAPI(
    title="SouqAI Intelligence Service",
    description="Microservice managing LangGraph conversational search.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(chat_router.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "intelligence_svc"}
