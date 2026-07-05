from src.core.entities.user import User, UserRole
from src.application.interfaces.user_repository import UserRepository
from src.infrastructure.security.auth_service import AuthService

class RegisterUserUseCase:
    """Use case for registering a new user."""
    
    def __init__(self, repo: UserRepository):
        self.repo = repo
        
    async def execute(self, email: str, password: str, role: str) -> User:
        # 1. Check if user already exists
        existing_user = await self.repo.get_by_email(email)
        if existing_user:
            raise ValueError("Email already registered")
            
        # 2. Hash password
        hashed = AuthService.get_password_hash(password)
        
        # 3. Create Entity
        try:
            user_role = UserRole(role.upper())
        except ValueError:
            raise ValueError(f"Invalid role: {role}")
            
        user = User(
            email=email,
            hashed_password=hashed,
            role=user_role,
            nafath_verified=False
        )
        user.validate()
        
        # 4. Save to Repository
        return await self.repo.create(user)
