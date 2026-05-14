from pypdf import PdfReader
import ollama
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import uuid

# Qdrant (local)
qdrant = QdrantClient(path="qdrant_db")

collection_name = "robotics_book"

# -------- TEXT CHUNKING --------
def chunk_text(text, size=500):
    chunks = []
    for i in range(0, len(text), size):
        chunks.append(text[i:i+size])
    return chunks


# -------- READ PDF --------
reader = PdfReader("book.pdf")

text = ""
for page in reader.pages:
    if page.extract_text():
        text += page.extract_text()

chunks = chunk_text(text)

# -------- CREATE COLLECTION (if not exists) --------
try:
    qdrant.get_collection(collection_name)
    print("Collection already exists ✅")
except:
    qdrant.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=768,  # nomic-embed-text size
            distance=Distance.COSINE
        )
    )
    print("Collection created ✅")


# -------- CREATE EMBEDDINGS --------
points = []

for chunk in chunks:
    embedding = ollama.embeddings(
        model="nomic-embed-text",
        prompt=chunk
    )["embedding"]

    points.append(
        PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={"text": chunk}
        )
    )

# -------- UPSERT DATA --------
qdrant.upsert(
    collection_name=collection_name,
    points=points
)

print("✅ PDF stored successfully!")