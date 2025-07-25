from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from chatbot import build_chatbot

app = FastAPI()

# Serve frontend files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def serve_home():
    return FileResponse("frontend/index.html")

# Enable CORS (for development, allow everything)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chatbot = build_chatbot()

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
async def chat(req: ChatRequest):
    answer = chatbot.run(req.question)
    return {"answer": answer}
