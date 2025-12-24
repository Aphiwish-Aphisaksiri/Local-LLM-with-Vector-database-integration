# Local-LLM-with-Vector-database-integration

This project demonstrates how to run a local Large Language Model (LLM) with vector database integration, providing a RESTful API (FastAPI) and a React-based chat UI.

## Requirements

### Python Backend
- Docker (recommended for easy setup)
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- [fastapi](https://fastapi.tiangolo.com/)
- [uvicorn](https://www.uvicorn.org/)
- [sentence-transformers](https://www.sbert.net/)
- [chromadb](https://www.trychroma.com/)
- [pdfplumber](https://github.com/jsvine/pdfplumber) (for PDF ingestion)

### React Frontend
- Node.js (v16+ recommended)
- npm

### Model File
- Download a GGUF model (e.g., TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf) from [HuggingFace](https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF)
- Place it in the `models/` folder (create if missing)

## Setup

### 1. Download Model
- Download a GGUF model file (see above)
- Place it in `models/` (e.g., `models/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf`)

### 2. Vector Database Setup (Optional)
To ingest a PDF and create a ChromaDB collection:

```cmd
python pdf_to_chromadb.py
```
This will create a persistent vector DB in `chroma_db/`.

### 3. Build Docker Image

Make sure Docker is installed and running.  
Build the Docker image from the project root:

```sh
docker build -t local-llm-app .
```

## Running

### 1. Start FastAPI Server with Docker

Run the container (it will automatically remove itself after stopping):

```sh
docker run --rm -p 8000:8000 local-llm-app
```

The server will be available at `http://localhost:8000`.

### 2. Start React Chat UI

```cmd
cd chatbot-ui
npm install
npm start
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

## Notes
- The `models/` folder is required but model files are not tracked in git (see `.gitignore`).
- For more details on llama-cpp-python, see: https://github.com/abetlen/llama-cpp-python