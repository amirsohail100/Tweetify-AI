from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Union
import json

from src.backend import generate_social_posts
from langchain_core.messages import HumanMessage, AIMessage

app = FastAPI(title="Tweetify AI", version="2.0")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

session_storage: Dict[str, List[Any]] = {
    "chat_history": []
}

class GenerateRequest(BaseModel):
    text_input: str = Field(
        ...,
        description="Input text for the AI to generate social posts.",
        min_length=1,
        max_length=10000,
    )

class SocialPostsResponse(BaseModel):
    linkedin: str
    twitter: List[str]
    instagram: str

@app.get("/",response_class=HTMLResponse)
async def serve_ui(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

@app.post("/api/generate", response_model=SocialPostsResponse)
async def generate_posts(payload: GenerateRequest):
    text = payload.text_input
    if not text:
        raise HTTPException(status_code=400, detail="Please provide a valid input text.")
    
    try:
        result = generate_social_posts(payload.text_input, session_storage["chat_history"])
        
        # Update chat history safely
        session_storage["chat_history"].append(HumanMessage(content=payload.text_input))
        session_storage["chat_history"].append(AIMessage(content=json.dumps(result)))
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/clear")
async def clear_session():
    session_storage["chat_history"] = []
    return {"status": "success", "message": "Chat history cleared successfully!"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port)