from src.application.interfaces.user_repository import UserRepository
from src.infrastructure.security.auth_service import AuthService

class AuthenticateUserUseCase:
    """Use case for authenticating a user and returning a JWT."""
    
    def __init__(self, repo: UserRepository):
        self.repo = repo
        
    async def execute(self, email: str, password: str) -> str:
        # 1. Retrieve user
        user = await self.repo.get_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")
            
        # 2. Verify password
        if not AuthService.verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")
            
        # 3. Generate JWT
        access_token = AuthService.create_access_token(
            data={"sub": user.id, "role": user.role.value, "nafath": user.nafath_verified}
        )
        return access_token
