from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import users, subscription, content, admin, admin_ai

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(subscription.router)
app.include_router(content.router)
app.include_router(admin.router)
app.include_router(admin_ai.router)

@app.get("/")
def home():
    return {"message": "Subscription API is running"}
