from database import SessionLocal
import models.user as models
from core.security import verify_password, create_access_token
from datetime import timedelta

try:
    print("Testing DB Connection...")
    db = SessionLocal()
    user = db.query(models.User).filter(models.User.email == "admin@souqai.com").first()
    if not user:
        print("User not found!")
    else:
        print("User found! Testing password verification...")
        is_valid = verify_password("password123", user.hashed_password)
        print(f"Password Valid: {is_valid}")
        
        print("Testing JWT creation...")
        token = create_access_token({"sub": user.email}, timedelta(minutes=30))
        print(f"Token: {token}")
except Exception as e:
    import traceback
    traceback.print_exc()
