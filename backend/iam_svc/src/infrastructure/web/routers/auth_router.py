from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.web.schemas import RegisterUserRequest, UserResponse, LoginRequest, TokenResponse, NafathWebhookRequest
from src.application.use_cases.register_user import RegisterUserUseCase
from src.application.use_cases.authenticate_user import AuthenticateUserUseCase
from src.application.use_cases.verify_nafath import VerifyNafathUseCase
from src.infrastructure.database.user_repo_impl import SQLAUserRepository

def get_db():
    pass

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    request: RegisterUserRequest, 
    db: Session = Depends(get_db)
):
    try:
        repo = SQLAUserRepository(db)
        use_case = RegisterUserUseCase(repo)
        
        user_entity = await use_case.execute(
            email=request.email,
            password=request.password,
            role=request.role
        )
        return user_entity
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponse)
async def login_user(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    try:
        repo = SQLAUserRepository(db)
        use_case = AuthenticateUserUseCase(repo)
        
        token = await use_case.execute(
            email=request.email,
            password=request.password
        )
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/nafath-callback", status_code=status.HTTP_200_OK)
async def nafath_webhook(
    request: NafathWebhookRequest,
    db: Session = Depends(get_db)
):
    if request.verification_status != "SUCCESS":
        raise HTTPException(status_code=400, detail="Verification not successful")
        
    try:
        repo = SQLAUserRepository(db)
        use_case = VerifyNafathUseCase(repo)
        
        await use_case.execute(user_id=request.user_id)
        return {"message": "Nafath verification successful"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
