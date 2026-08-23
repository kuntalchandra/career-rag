"""
Stages 5-6 of the RAG pipeline: retrieve, generate.
This is the real-time half. Run this any time, as many times as you want.

Generation now runs on Gemini instead of Claude. Notice that stage 5, retrieval,
is completely untouched below, only the generation call in stage 6 changed.
That separation is the whole point.
"""

import chromadb
from sentence_transformers import SentenceTransformer
from google import genai

TOP_K = 3


def main():
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection("interview_prep")

    gemini = genai.Client()  # reads GEMINI_API_KEY from the environment

    query = input("Ask a question about your career docs: ")

    print("\nStage 5: Retrieval")
    query_embedding = embedder.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K,
    )

    retrieved_chunks = results["documents"][0]
    sources = results["metadatas"][0]

    print(f"Top {TOP_K} matching chunks:")
    for chunk, meta in zip(retrieved_chunks, sources):
        preview = chunk[:80].replace("\n", " ")
        print(f"  - from {meta['source']}: {preview}...")

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""Answer the question using only the context below.
If the context doesn't contain the answer, say so honestly instead of guessing.

Context:
{context}

Question: {query}
"""

    print("\nStage 6: Generation")
    response = gemini.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    print("\nAnswer:")
    print(response.text)


if __name__ == "__main__":
    main()