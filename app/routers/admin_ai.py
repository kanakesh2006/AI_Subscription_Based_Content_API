from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, security
from app.ai.log_processor import get_logs_summary
from app.ai.graph import create_analysis_graph, create_nlq_graph

router = APIRouter(prefix="/admin/ai", tags=["admin_ai"])

# Dependency to ensure admin access
def check_admin(current_user: models.User = Depends(security.get_current_user)):
    # Simulating admin check
    return current_user

@router.get("/log-analysis")
def get_ai_analysis(db: Session = Depends(get_db), admin: models.User = Depends(check_admin)):
    try:
        logs_summary = get_logs_summary(db)
        graph = create_analysis_graph()
        
        inputs = {"logs_summary": logs_summary, "question": "", "result": ""}
        result = graph.invoke(inputs)
        
        return {"insights": result["result"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query")
def ai_query(
    question: str = Body(..., embed=True),
    db: Session = Depends(get_db), 
    admin: models.User = Depends(check_admin)
):
    try:
        logs_summary = get_logs_summary(db)
        graph = create_nlq_graph()
        
        inputs = {"logs_summary": logs_summary, "question": question, "result": ""}
        result = graph.invoke(inputs)
        
        return {"answer": result["result"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
