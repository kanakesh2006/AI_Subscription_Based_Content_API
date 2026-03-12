from sqlalchemy.orm import Session
from app import models
from collections import Counter
from datetime import datetime, timedelta

def get_logs_summary(db: Session):
    logs = db.query(models.AccessLog).all()
    if not logs:
        return "No activity logs found."

    total_accesses = len(logs)
    user_counts = Counter([log.user_id for log in logs])
    
    content_counts = Counter([log.content_id for log in logs])
    
    summary = [
        f"Total Premium Accesses: {total_accesses}",
        f"Unique Active Users: {len(user_counts)}",
        "\nTop Active Users:",
    ]
    
    for user_id, count in user_counts.most_common(5):
        user = db.query(models.User).filter(models.User.id == user_id).first()
        email = user.email if user else f"User {user_id}"
        summary.append(f"- {email}: {count} accesses")

    summary.append("\nTop Accessed Content:")
    for content_id, count in content_counts.most_common(5):
        content = db.query(models.Content).filter(models.Content.id == content_id).first()
        title = content.title if content else f"Content {content_id}"
        summary.append(f"- {title}: {count} views")

    # Add a simple time trend
    recent_logs = [log.access_time for log in logs if log.access_time > datetime.utcnow() - timedelta(days=1)]
    summary.append(f"\nActivity in last 24 hours: {len(recent_logs)} accesses")
    
    return "\n".join(summary)
