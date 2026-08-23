# RAG Study Plan — Progress Tracker

Goal: EM-level fluency in RAG — architecture, tradeoffs, data lifecycle, enough to build a toy version and reason credibly in an interview.

Environment: Chromebook, browser only. No local terminal on a laptop, but strong terminal fluency otherwise. Google Colab for quick concept exploration. GitHub Codespaces for anything project-level, since it gives a real terminal in the browser.

Anchor for grounding every concept: the Regression Analyzer built for Snabbit — CodeAnalyzer for diff parsing, EndpointMapper for AST-based structural indexing, RegressionAnalyzerAgent for the LLM reasoning layer.

---

## Plan adjustments made so far

- Day 5-6 originally assumes a local Python setup. Adjusted to run entirely in GitHub Codespaces instead, since ChromaDB and pip install work fine there and it matches tooling already in use.
- Generation swapped from Claude to Gemini, since Gemini has a genuine free tier with no minimum purchase, while both Anthropic and OpenAI require a $5 minimum to unlock full API access. Retrieval logic in query.py was untouched by this swap, only the final generation call changed, which itself became a live demonstration of why retrieval and generation are separate concerns.
- Model name gemini-2.5-flash was deprecated for new users mid-project. Fixed by switching to gemini-3.6-flash per Google's own error message. Worth remembering for future sessions: always check the current model name if this happens again.

---

## Day 5-6 notes — DONE

Built a working toy RAG pipeline in GitHub Codespaces, repo career-rag, private, MIT licensed for eventual public release, docs folder gitignored to keep personal documents out of git history.

Stack used: ChromaDB for local vector storage, sentence-transformers all-MiniLM-L6-v2 for embeddings, Gemini 3.6 Flash for generation.

Ran end to end successfully. Indexed 34 chunks across 4 documents, resume, cover letter, Regression Analyzer doc, and the hands-on storyboard. Query "What did I achieve at Allen Digital" correctly retrieved relevant resume and storyboard chunks via semantic search, no keyword overlap needed, and Gemini generated a grounded, accurate answer using only that retrieved text.

Debugging encountered and resolved along the way: query.py run before ingest.py, leading to an empty retrieval with no chunks found, fixed by running ingest.py first. Deprecated Gemini model name, fixed per the error message's own suggestion. Both are now understood, not just patched.

---

## Day-by-day status

- [x] Day 1-2 — Core Concepts — DONE
- [x] Day 3-4 — Architecture & Data Lifecycle — DONE
- [x] Day 5-6 — Hands-On Toy Project — DONE
- [ ] Day 7 — Tradeoffs, Scaling & EM Synthesis — NEXT

---

## Day 1-2 notes — DONE

Concepts covered: why RAG exists, embeddings, vector databases, chunking, the full pipeline flow.

Grounding used: EndpointMapper's AST-based index compared against a vector database's embedding-based index, to show what semantic retrieval adds over structural retrieval.

Output completed: 1-paragraph pipeline explanation, load through generate, refined across three drafts. Early drafts confused tokens with chunks, chunks with vectors, and the embedding model with the generation LLM. Final version is accurate and interview-ready. This is the answer skeleton for "walk me through RAG."

**Final answer:**

The RAG pipeline has 6 stages. It takes a user query and answers it using an external knowledge base. First, the knowledge base gets loaded as raw documents. Those documents get split into overlapping chunks made of tokens. The chunks overlap each other, not the tokens. This overlap means that even if a sentence gets cut between two chunks, each chunk still keeps enough meaning on its own. Each chunk then gets embedded into a vector using an embedding model. The same embedding model is later used to turn the user's query into a vector too, so the two stay comparable. The vectors get stored in a database, such as ChromaDB, along with an index. Loading, chunking, embedding, and storing all happen offline. If a document is new or updated, only that document gets re-indexed, not the whole knowledge base. When a user sends a query, it gets converted into a vector using that same embedding model. The system compares this query vector against the stored vectors using semantic search and pulls out the top-k closest chunks. Those chunks, the actual text, get added to the prompt. The LLM then generates an answer grounded in that retrieved text, so the answer stays relevant and accurate to the query.

---

## Day 3-4 notes — DONE

Concepts covered: ingestion pipeline design, index invalidation on updates and deletes, freshness versus staleness tradeoffs, data lifecycle management including embedding version changes and schema changes, chunk-level access control for privileged legal documents, and retrieval quality including recall versus precision, re-ranking, and hybrid search with BM25.

Grounding used: the Regression Analyzer's GitHub Action, triggered on PR and comment events, as the automated-trigger half of an ingestion pipeline. TTL caching work compared against freshness versus staleness. EndpointMapper's index breaking on schema drift compared against embedding version mismatches breaking vector search silently.

Output completed: 1-paragraph design for chunk-level access control in a legal document corpus, refined across three drafts. Early drafts recapped the six-stage pipeline instead of answering the question, and left ambiguous whether filtering happened before or after retrieval. Final version is precise: tag at ingestion following the platform's existing permission model, filter before similarity search so restricted chunks never enter the candidate pool.

**Final answer:**

Chunk-level access control: While the chunking is done by the pipeline, at that time only, the access tag gets determined by following the existing permission model of the platform and is tagged with each of the chunks. This helps to determine the visibility and the accessibility when retrieval comes into action. RBAC helps to determine the access of different roles eligible to access a certain chunk, e.g., a client-facing role will be restricted from accessing a chunk which is only tagged with privileged-users. Based on the access tag, only the permissible chunks get retrieved to be compared with the query vectors. So, the filtering happens even before the semantic search comes into action to ensure the retrieval doesn't get a restricted-tagged chunk to compare while retrieving. So, filtering the chunks even before retrieval and the similarity search ensures that any privileged chunk doesn't come to the possible candidate pool at all.

Optional strengthening, not yet added: an explicit line stating that tagging happens per chunk rather than per document, so a single document can mix privileged and non-privileged sections without either forcing the whole document out of reach.

covers — this file only tracks where we are.
