from typing import Optional
from sqlalchemy.orm import Session
from src.core.entities.user import User
from src.application.interfaces.user_repository import UserRepository
from src.infrastructure.database.models import UserModel

class SQLAUserRepository(UserRepository):
    """Concrete implementation of UserRepository using SQLAlchemy."""
    
    def __init__(self, db_session: Session):
        self.db = db_session
        
    async def create(self, user: User) -> User:
        db_user = UserModel(
            id=user.id,
            email=user.email,
            hashed_password=user.hashed_password,
            role=user.role,
            nafath_verified=user.nafath_verified,
            trust_score=user.trust_score,
            created_at=user.created_at
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return user
        
    def _to_entity(self, db_user: UserModel) -> User:
        return User(
            id=db_user.id,
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            role=db_user.role,
            nafath_verified=db_user.nafath_verified,
            trust_score=db_user.trust_score,
            created_at=db_user.created_at
        )

    async def get_by_id(self, user_id: str) -> Optional[User]:
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_entity(db_user) if db_user else None

    async def get_by_email(self, email: str) -> Optional[User]:
        db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_entity(db_user) if db_user else None

    async def update(self, user: User) -> User:
        db_user = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if db_user:
            db_user.email = user.email
            db_user.hashed_password = user.hashed_password
            db_user.role = user.role
            db_user.nafath_verified = user.nafath_verified
            db_user.trust_score = user.trust_score
            self.db.commit()
            self.db.refresh(db_user)
        return user
