import pdfplumber
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import os

# --- Step 2: Extract text from PDF ---
pdf_path = "BCI-report.pdf"  # Change to your PDF filename
all_text = ""
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        all_text += page.extract_text() + "\n"

# --- Step 3: Chunk the text ---

# Reduce chunk size to 200 words for smaller context
def chunk_text(text, max_words=200):
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i+max_words])
        chunks.append(chunk)
    return chunks

chunks = chunk_text(all_text, max_words=200)

# --- Step 4: Generate embeddings ---
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(chunks, show_progress_bar=True)

directory = "E:\\.Homeworks\\Life CH1\\Code\\LLM\\chroma_db"
print("ChromaDB persist_directory:", directory)

# --- Step 5: Store in ChromaDB ---
# Create a persistent ChromaDB collection in ./chroma_db

chroma_client = chromadb.PersistentClient(path=directory)
print("ChromaDB client created.")
collection = chroma_client.get_or_create_collection("capstone_pdf")
print("Collection obtained.")

# Add chunks and embeddings to the collection

for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
    collection.add(
        documents=[chunk],
        embeddings=[embedding],
        ids=[f"chunk_{idx}"]
    )
    if idx == 0:
        print("First chunk added.")
    if idx == len(chunks) - 1:
        print("Last chunk added.")

# List all collections to verify
print("Collections in DB:", chroma_client.list_collections())

#chroma_client.persist()
print("ChromaDB persisted to disk.")

print(f"Inserted {len(chunks)} chunks into ChromaDB collection 'capstone_pdf'.")
print("ChromaDB directory should be at:", directory)
print("Directory exists:", os.path.exists(directory))
if os.path.exists(directory):
    print("Directory contents:", os.listdir(directory))