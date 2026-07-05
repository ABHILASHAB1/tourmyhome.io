from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.web.schemas import CreateListingRequest, UpdateListingRequest, ListingResponse
from src.application.use_cases.create_listing import CreateListingUseCase
from src.application.use_cases.get_listing import GetListingUseCase
from src.application.use_cases.update_listing import UpdateListingUseCase
from src.application.use_cases.delete_listing import DeleteListingUseCase
from src.infrastructure.database.listing_repo_impl import SQLAListingRepository
from src.infrastructure.messaging.kafka_publisher import KafkaEventPublisher

def get_db():
    pass

def get_current_user_id() -> str:
    return "user-123"

# Singleton publisher instance
publisher_instance = KafkaEventPublisher()

router = APIRouter(prefix="/api/v1/listings", tags=["listings"])

@router.post("/", response_model=ListingResponse, status_code=status.HTTP_201_CREATED)
async def create_listing(
    request: CreateListingRequest, 
    db: Session = Depends(get_db),
    seller_id: str = Depends(get_current_user_id)
):
    try:
        # 1. Instantiate the Repository (Outbound Adapter)
        repo = SQLAListingRepository(db)
        
        # 2. Instantiate the Use Case (Application Logic)
        use_case = CreateListingUseCase(repo, publisher_instance)
        
        # 3. Execute the Use Case
        listing_entity = await use_case.execute(
            seller_id=seller_id,
            title=request.title,
            description=request.description,
            price_sar=request.price_sar,
            category_id=request.category_id
        )
        
        # 4. Map back to DTO
        return listing_entity
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{listing_id}", response_model=ListingResponse)
async def get_listing(
    listing_id: str,
    db: Session = Depends(get_db)
):
    repo = SQLAListingRepository(db)
    use_case = GetListingUseCase(repo)
    listing = await use_case.execute(listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

@router.put("/{listing_id}", response_model=ListingResponse)
async def update_listing(
    listing_id: str,
    request: UpdateListingRequest,
    db: Session = Depends(get_db),
    seller_id: str = Depends(get_current_user_id)
):
    repo = SQLAListingRepository(db)
    use_case = UpdateListingUseCase(repo, publisher_instance)
    try:
        listing = await use_case.execute(
            listing_id=listing_id,
            user_id=seller_id,
            title=request.title,
            description=request.description,
            price_sar=request.price_sar,
            status=request.status,
            category_id=request.category_id
        )
        return listing
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_listing(
    listing_id: str,
    db: Session = Depends(get_db),
    seller_id: str = Depends(get_current_user_id)
):
    repo = SQLAListingRepository(db)
    use_case = DeleteListingUseCase(repo, publisher_instance)
    try:
        await use_case.execute(listing_id, seller_id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
