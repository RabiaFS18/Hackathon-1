import os
import ollama
from rag_utils import chunk_text
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

DOCS_PATH = "../robotics-book/docs"

# connect to Qdrant (local memory)
qdrant = QdrantClient(path="qdrant_db")
collection_name = "robotics_book"


def load_docs():
    docs = []

    for file in os.listdir(DOCS_PATH):
        if file.endswith(".md"):
            with open(os.path.join(DOCS_PATH, file), "r", encoding="utf-8") as f:
                docs.append(f.read())

    return docs


# create collection
qdrant.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
)

docs = load_docs()

points = []
id_counter = 1

for doc in docs:

    chunks = chunk_text(doc)

    for chunk in chunks:

        embedding = ollama.embeddings(
            model="nomic-embed-text",
            prompt=chunk
        )

        vector = embedding["embedding"]

        points.append(
            PointStruct(
                id=id_counter,
                vector=vector,
                payload={"text": chunk}
            )
        )

        id_counter += 1


# upload embeddings
qdrant.upsert(
    collection_name=collection_name,
    points=points
)

print("Docs successfully stored in Qdrant!")