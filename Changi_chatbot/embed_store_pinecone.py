import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone
from tqdm import tqdm

# ---- Load API keys and region from .env ----
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_REGION = os.getenv("PINECONE_REGION")

INDEX_NAME = "changi-jewel-index"

def read_text(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def split_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_text(text)

def embed_and_store(chunks):
    print("🔄 Loading 1024-dim embedding model...")
    model = SentenceTransformer("WhereIsAI/UAE-Large-V1")

    print("📐 Creating embeddings...")
    embeddings = model.encode(chunks, show_progress_bar=True)

    print("🔗 Connecting to Pinecone...")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(INDEX_NAME)

    print(f"⬆️ Upserting {len(chunks)} chunks to Pinecone...")
    for i, (vector, text) in enumerate(tqdm(zip(embeddings, chunks), total=len(chunks))):
        index.upsert([
            (f"id-{i}", vector.tolist(), {"text": text})
        ])

    print("✅ Done. Embeddings stored in Pinecone!")

if __name__ == "__main__":
    full_text = read_text("scraped_data.txt")
    chunks = split_text(full_text)
    embed_and_store(chunks)
