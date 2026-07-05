from fastapi import FastAPI
from src.infrastructure.web.routers import auth_router

app = FastAPI(
    title="SouqAI IAM Service",
    description="Identity and Access Management microservice.",
    version="1.0.0"
)

app.include_router(auth_router.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "iam_svc"}
