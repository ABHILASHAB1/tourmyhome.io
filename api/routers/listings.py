from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models.listing as models
import schemas.listing as schemas

router = APIRouter(
    prefix="/api/v1/listings",
    tags=["listings"],
)

@router.get("/", response_model=List[schemas.Listing])
def read_listings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all listings.
    """
    listings = db.query(models.Listing).offset(skip).limit(limit).all()
    return listings

@router.post("/", response_model=schemas.Listing)
def create_listing(listing: schemas.ListingCreate, db: Session = Depends(get_db)):
    """
    Create a new listing.
    """
    db_listing = models.Listing(**listing.model_dump())
    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return db_listing

@router.get("/{listing_id}", response_model=schemas.Listing)
def read_listing(listing_id: int, db: Session = Depends(get_db)):
    """
    Get a specific listing by ID.
    """
    db_listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if db_listing is None:
        raise HTTPException(status_code=404, detail="Listing not found")
    return db_listing
