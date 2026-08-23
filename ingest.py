"""
Stages 1-4 of the RAG pipeline: load, chunk, embed, store.
This is the offline half. Run this once, and again whenever your docs change.
"""

import os
import chromadb
from sentence_transformers import SentenceTransformer

DOCS_FOLDER = "docs"
CHUNK_SIZE = 200       # words per chunk, standing in for tokens to keep this dependency-free
CHUNK_OVERLAP = 30     # words shared between consecutive chunks


def load_documents(folder):
    """Stage 1: Load. Reads every .txt file in the docs folder as raw text."""
    documents = []
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            path = os.path.join(folder, filename)
            with open(path, "r", encoding="utf-8") as f:
                documents.append({"source": filename, "text": f.read()})
    return documents


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Stage 2: Chunk. Splits text into overlapping word-based chunks."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def main():
    print("Stage 1: Loading documents from ./docs")
    documents = load_documents(DOCS_FOLDER)
    print(f"Loaded {len(documents)} document(s)")

    print("Stage 2 and 3: Chunking and loading the embedding model")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    print("Stage 4: Opening ChromaDB, stored locally in ./chroma_db")
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection("interview_prep")

    chunk_id = 0
    for doc in documents:
        chunks = chunk_text(doc["text"])
        print(f"  {doc['source']}: {len(chunks)} chunk(s)")
        for chunk in chunks:
            embedding = embedder.encode(chunk).tolist()
            collection.add(
                ids=[f"chunk_{chunk_id}"],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{"source": doc["source"]}],
            )
            chunk_id += 1

    print(f"\nDone. Indexed {chunk_id} chunk(s) into ChromaDB.")


if __name__ == "__main__":
    main()
