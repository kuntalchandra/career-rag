# RAG Fundamentals → Depth: 1-Week Plan
**Goal:** EM-level fluency — can discuss architecture, tradeoffs, data lifecycle, and lead a team through it. Not hands-on implementation depth, but enough to build a toy version and reason credibly in an interview.

---

## Day 1-2 — Core Concepts
**What to cover:**
- Why RAG exists: LLMs have knowledge cutoffs + no access to private data. RAG retrieves relevant external content at query time and injects it into the prompt.
- **Embeddings** — text → vectors capturing semantic meaning (not keyword match)
- **Vector databases** — where embeddings live, how similarity search works (Pinecone, Weaviate, Chroma, pgvector)
- **Chunking** — why documents are split before embedding; tradeoff between small chunks (precise, less context) and large chunks (context-rich, noisier)
- **The pipeline flow:** query → embed → similarity search → top-k chunks retrieved → injected into prompt → LLM generates grounded answer

**Resources:**
- [RAG Pipeline Tutorial — MyEngineeringPath](https://myengineeringpath.dev/programming/python/rag-pipeline-tutorial/) — good for "why build from scratch" framing + interview Q&A section built in
- Original RAG paper (Lewis et al., 2020) — 10-page intro, worth skimming even at EM level for the "why" grounding
- [How to Build a RAG Pipeline: 12 Steps, 90 Min](https://tech-insider.org/how-to-build-a-rag-pipeline-2026/) — concise walkthrough of the 6 stages

**Output for Day 1-2:** Write a 1-paragraph explanation, in your own words, of the full pipeline (load → chunk → embed → store → retrieve → generate). This is your interview answer skeleton for "walk me through RAG."

---

## Day 3-4 — Architecture & Data Lifecycle (the JD's named requirement — go deepest here)
**What to cover:**
- **Ingestion pipeline** — how source docs get processed, chunked, embedded, indexed; what happens on updates/deletes (re-embedding, index invalidation)
- **Freshness/staleness tradeoffs** — real-time vs batch re-indexing, cost/latency implications
- **Data lifecycle management** — versioning embeddings, schema changes, deprecating stale vectors, chunk-level access control (**highly relevant for Harvey** — legal docs have confidentiality/privilege boundaries; this is a natural bridge point in an interview)
- **Retrieval quality** — recall/precision tradeoffs, re-ranking, hybrid search (vector + keyword/BM25)

**Resources:**
- [Kapa.ai — Building a Robust RAG Pipeline in 2026](https://www.kapa.ai/blog/how-to-build-a-rag-pipeline-from-scratch-in-2026) — production-lens, good for lifecycle/reliability angle
- [RAG Tutorial 2026 — AIToolRanked](https://aitoolranked.com/blog/rag-tutorial-beginners-2026-complete-guide) — covers Naive RAG → Hybrid RAG → Graph RAG → Agentic RAG spectrum, useful for "when does RAG break down" framing

**Output for Day 3-4:** One paragraph specifically on how you'd design chunk-level access control for a legal document corpus. This is a strong, Harvey-specific talking point — shows you've thought about their actual domain, not generic RAG.

---

## Day 5-6 — Hands-On Toy Project
**Build a minimal RAG pipeline over your own interview prep documents** (storyboards, resume, prior screening answers). Practical, memorable, and gives you something real to reference in interviews ("I actually built a small RAG system over my own career docs to understand this").

**Stack:** Python + ChromaDB (free, local, no infra setup) + OpenAI or Claude API for generation

**Steps (~90 min per the tutorial below, spread across 2 days is fine):**
1. Load your docs (resume, storyboards) as text
2. Chunk them (start with ~500 tokens, 50 overlap)
3. Generate embeddings for each chunk
4. Store in ChromaDB
5. Write a query function: embed the question → retrieve top-3 chunks → pass to LLM with the question → get grounded answer
6. Test it: ask "What did I achieve at Ula?" and see if it retrieves the right chunk and answers correctly

**Resource:**
- [RAG Pipeline: 12 Steps, 90 Min](https://tech-insider.org/how-to-build-a-rag-pipeline-2026/) — exact step-by-step for this
- [RAG Tutorial — LangChain + ChromaDB](https://nandigamharikrishna.substack.com/p/rag-tutorial-build-a-retrieval-augmented) — alternative walkthrough if you want a framework-based version instead of raw Python

I can help you write this code directly when you're ready — just say so and we'll build it together in a session.

---

## Day 7 — Tradeoffs, Scaling & EM Synthesis
**What to cover:**
- Cost/latency tradeoffs at scale (vector DB query cost grows with corpus size)
- Where RAG breaks down: multi-hop reasoning, synthesizing across many documents rather than a few retrieved chunks — this is where Graph RAG / Agentic RAG enter the conversation
- **EM framing (this is what actually gets asked):**
  - What you'd own as an EM vs. what's a specialized ML/infra function
  - How you'd staff/hire for this
  - Build vs. buy: managed vector DB (Pinecone) vs. self-hosted (pgvector, Weaviate)
  - How you'd measure retrieval quality on an ongoing basis (RAGAS-style metrics: faithfulness, answer relevancy, context recall)

**Output for Day 7:** Draft answers to these two likely interview questions:
1. "Walk me through how you'd architect a RAG pipeline for a legal document platform."
2. "How would you know if your RAG system's retrieval quality was degrading, and what would you do about it?"

Send me your draft answers and I'll pressure-test them the way we do with your screening responses — tight, outcome-driven, no hand-waving.

---

## Notes
- This is EM-depth, not ML-engineer depth. You don't need to hand-derive embedding math — you need to reason about architecture, tradeoffs, and lifecycle like someone who'd lead the team building it.
- The Harvey-specific bridge (chunk-level access control for privileged legal documents) is your strongest differentiator — most candidates won't connect RAG lifecycle management to legal confidentiality requirements. Use it.
