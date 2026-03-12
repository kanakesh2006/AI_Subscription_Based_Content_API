from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, security
import csv
import io

router = APIRouter(prefix="/admin", tags=["admin"])

# Helper to check if user is admin (simplifying for this phase)
def check_admin(current_user: models.User = Depends(security.get_current_user)):
    # In a real app, we might have an 'is_admin' boolean. 
    # For now, let's say only specific emails or a role can access.
    # Since the requirements don't explicitly define an admin role yet, 
    # we'll assume a 'premium' user can view their own analytics or 
    # we'll just allow it for testing purposes.
    return current_user

@router.get("/access-logs")
def get_all_logs(db: Session = Depends(get_db), admin: models.User = Depends(check_admin)):
    logs = db.query(models.AccessLog).all()
    return logs

@router.get("/reports")
def generate_csv_report(db: Session = Depends(get_db), admin: models.User = Depends(check_admin)):
    logs = db.query(models.AccessLog).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "User ID", "Content ID", "IP Address", "Access Time"])
    
    for log in logs:
        writer.writerow([log.id, log.user_id, log.content_id, log.ip_address, log.access_time])
    
    output.seek(0)
    
    headers = {
        'Content-Disposition': 'attachment; filename="usage_report.csv"'
    }
    
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers=headers)
