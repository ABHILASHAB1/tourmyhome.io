from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import listings, search, auth
import models.listing as models
from database import engine

# Create the database tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SouqAI KSA API",
    description="Enterprise backend for SouqAI classifieds marketplace",
    version="1.0.0"
)

# Enable CORS for the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(auth.router)
app.include_router(listings.router)
app.include_router(search.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to SouqAI KSA Enterprise API",
        "docs_url": "/docs"
    }
