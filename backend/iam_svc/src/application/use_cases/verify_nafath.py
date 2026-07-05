from src.application.interfaces.user_repository import UserRepository

class VerifyNafathUseCase:
    """Use case for simulating a Nafath webhook callback that verifies a user's identity."""
    
    def __init__(self, repo: UserRepository):
        self.repo = repo
        
    async def execute(self, user_id: str) -> bool:
        # 1. Retrieve user
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
            
        # 2. Update Nafath status
        user.nafath_verified = True
        
        # 3. Save to Repository
        await self.repo.update(user)
        
        return True
