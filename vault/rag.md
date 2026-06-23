# Retrieval Augmented Generation
RAG combines retrieval with generation so answers can lean on source material instead of model memory.
## 1. Why RAG exists
- RAG lowers hallucination by grounding outputs in retrieved evidence.
- It helps models answer with fresher context than the pretraining cutoff.
- It keeps domain knowledge external, which makes updates cheaper.
- It supports citations, traceability, and user trust.
- It works well when the answer lives inside documents, tickets, or notes.
- It is useful when memorizing everything inside the model would be inefficient.
- It is often the fastest way to add domain knowledge to an LLM app.
- It separates search problems from language generation problems.
- It gives teams a path to improve quality without retraining the base model.
## 2. Data preparation
- Start with clean source documents and remove obvious duplicates.
- Normalize headings, spacing, and broken formatting before indexing.
- Preserve metadata such as title, author, date, and source path.
- Track document version so retrieval can explain which revision was used.
- Decide which content should be excluded for privacy or policy reasons.
- Keep the original text alongside the processed chunks.
- Convert tables and lists into a stable text representation.
- Record language and file type to support downstream filtering.
- Build ingestion logs so you can debug missing or malformed records.
## 3. Chunking
- Chunking should respect semantic boundaries instead of raw character count only.
- Smaller chunks improve precision but may lose surrounding context.
- Larger chunks preserve context but can dilute retrieval relevance.
- Use overlap when ideas span adjacent sections.
- Split by headings, paragraphs, or sentence groups when possible.
- Avoid cutting tables, code samples, or formulas in the middle.
- Tune chunk size against your model context window and retrieval latency.
- Keep chunk identifiers stable so you can reproduce results.
- Test chunking on real queries, not only on synthetic examples.
## 4. Embeddings and indexes
- Embeddings map text into vectors that can be compared quickly.
- Choose an embedding model that matches the language and domain.
- Store chunk text, vector, and metadata together in the index.
- Use approximate nearest neighbor search for scale and latency.
- Add metadata filters for source, date, tenant, or document type.
- Re-embed when the embedding model changes materially.
- Normalize text consistently before embedding to reduce drift.
- Measure recall with a labeled query set to find blind spots.
- Keep index rebuilds predictable so updates do not surprise users.
## 5. Retrieval strategies
- Similarity search is the baseline, but not always the best final answer.
- Hybrid retrieval can combine vector search with keyword matching.
- Metadata filters help narrow search before ranking results.
- Query rewriting can improve recall when the user asks vaguely.
- Multi-hop retrieval is useful when one document points to another.
- Re-ranking can promote the most useful chunks after initial retrieval.
- Diversity matters when the answer needs multiple viewpoints.
- Top-k should be tuned against context budget, not chosen arbitrarily.
- Retrieval logs should show why each chunk was returned.
## 6. Prompt assembly
- Put retrieved evidence in a clear, bounded section of the prompt.
- Label sources so the model can distinguish evidence from instructions.
- Limit the number of chunks to fit the context window comfortably.
- Remove redundant chunks when they repeat the same claim.
- Order chunks by relevance and then by narrative flow.
- Use explicit instructions to answer only from provided context when needed.
- Ask the model to cite sources if the product requires traceability.
- Reserve room for the user query and the model response.
- Keep prompt templates simple enough to debug by inspection.
## 7. Answer generation
- Generation should reflect retrieved evidence rather than free association.
- If evidence is weak, the system should say so instead of guessing.
- Answers should match the evidence language and scope.
- The model can synthesize across chunks when facts align.
- A good answer distinguishes facts, inferences, and uncertainty.
- Long answers benefit from sectioned output and concise summaries.
- For user trust, surface the source path or document title when possible.
- When retrieval fails, return a graceful fallback or a clarification request.
- Avoid overconfident phrasing when the context is partial.
## 8. Evaluation
- Evaluate retrieval and generation separately so failures are easier to isolate.
- Build a query set that reflects real user intent.
- Measure recall, precision, answer correctness, and citation quality.
- Include negative tests where the answer should be unavailable.
- Compare the system against a no-retrieval baseline.
- Review failures manually to see whether the issue is chunking, indexing, or prompting.
- Track latency and cost alongside quality metrics.
- Re-run evaluation after every major content or model change.
- Keep a small gold set for regression testing.
## 9. Ops and monitoring
- Monitor ingestion freshness so stale content is visible.
- Log which documents were consulted for every user request.
- Watch for retrieval drift when the document corpus changes.
- Track cache hit rates if you cache embeddings or search results.
- Set alerts for empty retrievals or sudden quality drops.
- Protect sensitive content with access controls before retrieval.
- Audit prompt templates because small changes can shift behavior.
- Keep feature flags for model, retrieval, and chunking changes.
- Review failure cases on a recurring schedule.
## 10. Failure patterns and fixes
- If answers drift, check whether the context is noisy or irrelevant.
- If retrieval misses the answer, inspect chunking and query wording first.
- If the model copies too much text, tighten output instructions.
- If the system hallucinates, reduce context noise and improve grounding.
- If the answer is incomplete, consider multi-hop retrieval or larger chunks.
- If latency is high, inspect index size, reranking, and prompt length.
- If updates are expensive, separate index refresh from model changes.
- If users do not trust the output, improve citations and source transparency.
- If quality is uneven, create a labeled review loop and iterate.
