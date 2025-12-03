
from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama
import sqlite3
from datetime import datetime
import uvicorn

from fastapi.middleware.cors import CORSMiddleware


# Path to your GGUF model
MODEL_PATH = "models/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf"  # Update as needed

llm = Llama(model_path=MODEL_PATH, n_ctx=2048)

app = FastAPI()

# Database setup
DB_PATH = "conversations.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    user_prompt TEXT,
    assistant_response TEXT,
    session_id TEXT
)
''')
conn.commit()

class ChatRequest(BaseModel):
    prompt: str
    history: list = []  # Optional: previous messages
    session_id: str = "default"  # Optional: to group conversations

@app.post("/chat")
async def chat(req: ChatRequest):
    # Optionally, build conversation context from history
    context = ""
    for turn in req.history:
        context += f"<|user|> {turn['user']}\n<|assistant|> {turn['assistant']}\n"
    context += f"<|user|> {req.prompt}\n<|assistant|>"
    output = llm(context, max_tokens=256, stop=["<|user|>", "<|assistant|>"])
    response = output["choices"][0]["text"].strip()
    # Save to database
    cursor.execute(
        "INSERT INTO conversations (timestamp, user_prompt, assistant_response, session_id) VALUES (?, ?, ?, ?)",
        (datetime.utcnow().isoformat(), req.prompt, response, req.session_id)
    )
    conn.commit()
    response = output["choices"][0]["text"].strip() if output["choices"][0]["text"].strip() else "No response generated."
    return {"response": response}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("chat_server:app", host="0.0.0.0", port=8000, reload=True)
