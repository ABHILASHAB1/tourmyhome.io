from fastapi import FastAPI
from src.infrastructure.web.routers import ws_router

app = FastAPI(
    title="SouqAI Messaging Service",
    description="Real-time WebSockets microservice.",
    version="1.0.0"
)

app.include_router(ws_router.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "messaging_svc"}
