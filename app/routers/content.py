from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, security
from datetime import datetime

router = APIRouter(prefix="/content", tags=["content"])

@router.get("/free")
def get_free_content():
    return {
        "title": "Welcome to the Platform",
        "body": "This is free content available to everyone. Register and upgrade to access premium features!"
    }

@router.get("/premium")
def get_premium_content(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    # Authorization Check
    if current_user.role != "premium":
        raise HTTPException(status_code=403, detail="Premium subscription required")
    
    # Expiry Check (Enhancement 1)
    if current_user.subscription_expiry and datetime.utcnow() > current_user.subscription_expiry:
        current_user.role = "free"
        db.commit()
        raise HTTPException(status_code=403, detail="Subscription expired. Please upgrade again.")

    # Activity Logging (Phase 6)
    log_entry = models.AccessLog(
        user_id=current_user.id,
        content_id=1,  # Mocking content ID for now
        ip_address=request.client.host,
        access_time=datetime.utcnow()
    )
    db.add(log_entry)
    db.commit()

    return {
        "title": "Exclusive Premium Content",
        "body": "Congratulations! You have access to this premium content because of your active subscription.",
        "logged_at": log_entry.access_time
    }
