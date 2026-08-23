# Career RAG

A minimal Retrieval-Augmented Generation pipeline, built to learn RAG hands-on by indexing my own career documents and answering questions grounded in them.

## What it does

The pipeline runs in two halves, matching the standard six-stage RAG flow.

**Offline, `ingest.py`:** load documents from `docs/`, chunk them with overlap, embed each chunk, store the vectors in ChromaDB.

**Real-time, `query.py`:** embed the incoming question with the same embedding model, retrieve the top matching chunks, generate a grounded answer with Claude.

## Stack

- ChromaDB, local vector storage
- sentence-transformers, `all-MiniLM-L6-v2`, for embeddings
- Gemini, for generation

## Setup

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Add a `GEMINI_API_KEY` as a Codespaces secret before running `query.py`.

## Usage

```
python ingest.py
python query.py
```

`ingest.py` prints each pipeline stage as it runs. `query.py` prints the retrieved chunks before the generated answer, so retrieval and generation stay visibly separate.

## Note on documents

The `docs/` folder is gitignored. It's meant to hold personal source material, resume, notes, prior answers, that shouldn't be committed to the repo. Drop your own `.txt` files in locally before running `ingest.py`.

## License

MIT
