from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
from datetime import datetime, timedelta
import random

def seed_data():
    db = SessionLocal()
    try:
        # 1. Ensure a user exists
        user = db.query(models.User).filter(models.User.email == "testing@gmail.com").first()
        if not user:
            user = models.User(
                email="testing@gmail.com",
                password_hash="dummy_hash", # Not for real login
                role="premium",
                subscription_expiry=datetime.utcnow() + timedelta(days=30)
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"Created user: {user.email}")
        else:
            # Ensure they are premium for better log simulation
            user.role = "premium"
            user.subscription_expiry = datetime.utcnow() + timedelta(days=30)
            db.commit()
            print(f"Found existing user: {user.email}")

        # 2. Create some content
        if db.query(models.Content).count() == 0:
            contents = [
                models.Content(title="AI Industry Report 2024", body="Deep dive into AI stats...", is_premium=True),
                models.Content(title="Market Analysis", body="Trends in fintech...", is_premium=True),
                models.Content(title="Free Guide", body="How to start coding...", is_premium=False)
            ]
            db.add_all(contents)
            db.commit()
            print("Created dummy content.")

        # 3. Create access logs
        all_contents = db.query(models.Content).filter(models.Content.is_premium == True).all()
        if not all_contents:
            print("No premium content found to log.")
            return

        print("Seeding logs...")
        for _ in range(20):
            random_content = random.choice(all_contents)
            # Random time in the last 7 days
            random_days = random.randint(0, 7)
            random_hours = random.randint(0, 23)
            access_time = datetime.utcnow() - timedelta(days=random_days, hours=random_hours)
            
            log = models.AccessLog(
                user_id=user.id,
                content_id=random_content.id,
                ip_address=f"192.168.1.{random.randint(1, 254)}",
                access_time=access_time
            )
            db.add(log)
        
        db.commit()
        print("Successfully seeded 20 access logs.")

    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
