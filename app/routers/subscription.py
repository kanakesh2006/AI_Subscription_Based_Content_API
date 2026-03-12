from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db
from app import models, schemas, security

router = APIRouter(prefix="/subscription", tags=["subscription"])

@router.post("/upgrade")
def upgrade_subscription(
    upgrade_data: schemas.SubscriptionUpgrade,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    if current_user.role == "premium":
        return {"message": "User is already a premium member", "expires": current_user.subscription_expiry}

    # Simulate payment process
    payment_successful = True  # Simulation
    
    if not payment_successful:
        raise HTTPException(status_code=402, detail="Payment required")

    # Update user role and expiry
    current_user.role = "premium"
    current_user.subscription_expiry = datetime.utcnow() + timedelta(days=30)
    
    db.commit()
    db.refresh(current_user)

    return {
        "message": "Subscription upgraded successfully",
        "expires": current_user.subscription_expiry.strftime("%Y-%m-%d")
    }
