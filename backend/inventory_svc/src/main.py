from fastapi import FastAPI
from src.infrastructure.web.routers import listing_router

app = FastAPI(
    title="SouqAI Inventory Service",
    description="Microservice managing listings and inventory, built with Clean Architecture.",
    version="1.0.0"
)

# Include Routers
app.include_router(listing_router.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "inventory_svc"}
