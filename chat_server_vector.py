from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama
from sentence_transformers import SentenceTransformer
from fastapi.middleware.cors import CORSMiddleware
import chromadb
import os

# --- Config ---
MODEL_PATH = "models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"  # Update as needed
CHROMA_DB_PATH = "chroma_db"
COLLECTION_NAME = "capstone_pdf"
EMBED_MODEL = "all-MiniLM-L6-v2" # SentenceTransformer model by HuggingFace

# --- Load LLM and Embedding Model ---
llm = Llama(model_path=MODEL_PATH, n_ctx=2048)
embedder = SentenceTransformer(EMBED_MODEL)

# --- Load ChromaDB ---
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = chroma_client.get_or_create_collection(COLLECTION_NAME)

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str
    history: list = []  # Optional: previous messages
    session_id: str = "default"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(req: ChatRequest):
    # 1. Embed the user prompt
    query_embedding = embedder.encode([req.prompt])[0]
    # 2. Search ChromaDB for top 3 relevant chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        include=["documents"]
    )
    retrieved_chunks = [doc for doc in results["documents"][0]]
    # 3. Build context from retrieved chunks
    context_text = "\n".join(retrieved_chunks)
    # 4. Build conversation history
    history_text = ""
    for turn in req.history:
        history_text += f"<|user|> {turn['user']}\n<|assistant|> {turn['assistant']}\n"
    # 5. Compose prompt for LLM
    full_prompt = (
        f"You are a helpful assistant with access to the following project context:\n"
        f"{context_text}\n"
        f"{history_text}"
        f"<|user|> {req.prompt}\n<|assistant|>"
    )
    # 6. Get LLM response
    output = llm(full_prompt, max_tokens=256, stop=["<|user|>", "<|assistant|>"])
    response = output["choices"][0]["text"].strip()
    return {"response": response, "context": retrieved_chunks}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("chat_server_vector:app", host="0.0.0.0", port=8000, reload=True)
