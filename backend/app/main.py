from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# ---------------- APP ----------------
app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- REQUEST MODEL ----------------
class ChatRequest(BaseModel):
    question: str
    selected_text: str = ""
    level: str = "beginner"
    language: str = "english"

# ---------------- HOME ROUTE ----------------
@app.get("/")
def home():
    return {
        "message": "Backend Running 🚀"
    }

# ---------------- CHAT ROUTE ----------------
@app.post("/chat")
def chat(request: ChatRequest):

    query = (
        request.selected_text
        if request.selected_text
        else request.question
    )

    # Demo AI response
    answer = f"""
🤖 AI Tutor Response

Question:
{query}

Level:
{request.level}

Language:
{request.language}

This is a demo response for your Physical AI & Humanoid Robotics textbook chatbot.

The chatbot integration, frontend UI, FastAPI backend, and API connection are working successfully.
"""

    return {
        "answer": answer
    }