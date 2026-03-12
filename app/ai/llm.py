from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY

def get_llm():
    if not GROQ_API_KEY:
        # We allow it to be None for setup, but it will fail at runtime if not provided
        pass
        
    return ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.1-8b-instant",
        temperature=0
    )
