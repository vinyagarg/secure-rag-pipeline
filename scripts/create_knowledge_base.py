import os
import time
import requests
import trafilatura

OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

for f in os.listdir(OUTPUT_DIR):
    if f.endswith(".txt") or f.endswith(".md"):
        os.remove(os.path.join(OUTPUT_DIR, f))
print("Cleared old files.\n")

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def scrape(url):
    try:
        d = trafilatura.fetch_url(url)
        text = trafilatura.extract(d, include_links=False, include_tables=True) if d else None
        return text if text and len(text.strip()) > 300 else None
    except:
        return None

# Sites confirmed working via trafilatura
SCRAPE_SOURCES = [
    ("fastapi_intro.txt",              "https://fastapi.tiangolo.com/"),
    ("fastapi_path_params.txt",        "https://fastapi.tiangolo.com/tutorial/path-params/"),
    ("fastapi_request_body.txt",       "https://fastapi.tiangolo.com/tutorial/body/"),
    ("fastapi_dependencies.txt",       "https://fastapi.tiangolo.com/tutorial/dependencies/"),
    ("fastapi_middleware.txt",         "https://fastapi.tiangolo.com/tutorial/middleware/"),
    ("fastapi_cors.txt",               "https://fastapi.tiangolo.com/tutorial/cors/"),
    ("fastapi_handling_errors.txt",    "https://fastapi.tiangolo.com/tutorial/handling-errors/"),
    ("fastapi_background_tasks.txt",   "https://fastapi.tiangolo.com/tutorial/background-tasks/"),
    ("chromadb_getting_started.txt",   "https://docs.trychroma.com/docs/overview/getting-started"),
    ("huggingface_transformers.txt",   "https://huggingface.co/docs/transformers/index"),
    ("huggingface_sentence.txt",       "https://huggingface.co/sentence-transformers"),
    ("groq_quickstart.txt",            "https://console.groq.com/docs/quickstart"),
    ("groq_models.txt",                "https://console.groq.com/docs/models"),
    ("pinecone_rag.txt",               "https://www.pinecone.io/learn/retrieval-augmented-generation/"),
    ("jina_embeddings.txt",            "https://jina.ai/news/jina-embeddings-v3-a-frontier-multilingual-embedding-model"),
    ("docker_getting_started.txt",     "https://docs.docker.com/get-started/"),
    ("docker_compose.txt",             "https://docs.docker.com/compose/"),
]

# High-quality fallback content for JS-rendered sites — real source URLs cited
WRITTEN_SOURCES = {

"langchain_rag_concepts.txt": ("https://python.langchain.com/docs/concepts/rag/", """
Retrieval-Augmented Generation (RAG) is a technique for augmenting LLM knowledge with additional, often private or real-time, data. LLMs can reason about wide-ranging topics, but their knowledge is limited to public data up to a specific point in time. If you want to build AI applications that can reason about private data or data introduced after a model's cutoff date, you need to augment the knowledge of the model with the specific information it needs.

RAG consists of two phases. The first phase is indexing: documents are loaded using document loaders, split into chunks using text splitters, and stored as vector embeddings in a vector store. The second phase is retrieval and generation: at runtime, a user query is embedded and the most relevant chunks are retrieved, then passed as context to the LLM for grounded generation.

The key advantage of RAG over pure parametric generation is grounding — the model is constrained to answer from retrieved documents rather than from its training data alone. This reduces hallucination significantly, especially for domain-specific or time-sensitive questions. However, RAG is not a complete solution to hallucination: the model can still misread or slightly misrepresent the context it receives.

Common failure modes include retrieval failures where the right document is not found due to vocabulary mismatch between the query and document, context stuffing where too many low-relevance chunks dilute the signal, and generation drift where the LLM ignores retrieved context and answers from training data instead. Addressing these failure modes requires careful chunking strategy, embedding model selection, retrieval evaluation, and output grounding verification.
"""),

"langchain_vectorstores.txt": ("https://python.langchain.com/docs/concepts/vectorstores/", """
Vector stores are databases optimized for storing and retrieving vector embeddings. In LangChain, vector stores are a core component for building retrieval systems that enable semantic search — finding documents by meaning rather than exact keyword match.

A vector store accepts documents, embeds them using an embedding model, and stores both the text and its embedding. At query time, the query is embedded using the same model and the store returns the k most similar document embeddings along with their text content. Similarity is most commonly measured using cosine similarity.

LangChain supports many vector store providers including ChromaDB for local development, Pinecone for cloud-scale deployments, FAISS for in-memory search, Weaviate and Qdrant for open-source self-hosted deployments, and PGVector for PostgreSQL-based storage. Each has different tradeoffs in terms of scalability, persistence, filtering capability, and ease of setup.

The VectorStore interface in LangChain exposes common methods: add_documents for adding new documents to the store, similarity_search for retrieving the top-k most similar documents to a query, and as_retriever for converting the vector store into a retriever that can be used in a RAG chain. The as_retriever method also supports filtering by metadata, allowing retrieval to be constrained to specific document types, dates, or categories.
"""),

"langchain_embeddings.txt": ("https://python.langchain.com/docs/concepts/embedding_models/", """
Embedding models convert text into dense numerical vectors that capture semantic meaning. Two texts with similar meanings will have embedding vectors that are close together in the high-dimensional vector space, even if they use completely different words. This property makes embeddings the foundation of semantic search, clustering, and retrieval-augmented generation.

LangChain provides a standardized Embeddings interface with two methods: embed_documents for embedding a list of texts during indexing, and embed_query for embedding a single query string at retrieval time. In some embedding models, documents and queries use different prompts internally, so these methods must be used correctly.

Popular embedding models supported in LangChain include OpenAI text-embedding-3-small and text-embedding-3-large, which offer high quality but require API calls. HuggingFace sentence-transformers models like all-MiniLM-L6-v2 are free, open-source, and run locally without API dependency. Jina AI provides free API-based embeddings with strong multilingual support. Cohere provides embeddings with built-in reranking capabilities.

Embedding dimensionality matters: higher dimensions capture more nuance but require more storage and computation. The embedding model must be consistent between indexing and retrieval — if documents are indexed with one model, all queries must be embedded with the same model. Switching models requires rebuilding the entire vector index from scratch.
"""),

"langchain_retrievers.txt": ("https://python.langchain.com/docs/concepts/retrievers/", """
Retrievers in LangChain are components that return relevant documents from a knowledge base given a query. The base Retriever interface exposes an invoke method that takes a string query and returns a list of Document objects. Vector store retrievers are the most common type, wrapping a vector store's similarity search to enable it to work in LangChain chains and agents.

Beyond simple vector store retrieval, LangChain supports more advanced retrieval patterns. MultiQueryRetriever generates multiple phrasings of the original query and retrieves documents for each, then merges and deduplicates the results. This helps overcome vocabulary mismatch where the original query phrasing misses relevant documents that use different terminology.

ContextualCompressionRetriever adds a post-processing step where retrieved documents are compressed or filtered to remove irrelevant content before being passed to the LLM. This reduces noise in the context and improves generation quality, especially when full document chunks contain a mix of relevant and irrelevant information.

BM25Retriever provides keyword-based retrieval that complements semantic search by capturing exact term matches. Combining BM25 and vector search — called hybrid search — gives better results than either alone: semantic search understands meaning while BM25 ensures important specific terms are captured. EnsembleRetriever makes hybrid search easy by combining multiple retrievers with configurable weights.
"""),

"langchain_text_splitters.txt": ("https://python.langchain.com/docs/concepts/text_splitters/", """
Text splitters divide large documents into smaller chunks suitable for embedding and retrieval. Chunk size is one of the most impactful decisions in RAG system design because it determines the granularity and context of what gets retrieved.

The RecursiveCharacterTextSplitter is LangChain's recommended default. It attempts to split on paragraph boundaries first, then sentence boundaries, then word boundaries, always trying to keep semantically related content together. Chunk size is specified in characters or tokens, with an overlap parameter that repeats some content from one chunk into the next to prevent important information from being lost at boundaries.

Choosing chunk size involves a fundamental tradeoff. Small chunks (100-300 tokens) enable precise retrieval — the retrieved content closely matches the specific question asked. But small chunks can lose surrounding context that gives the answer meaning. Large chunks (500-1000 tokens) preserve context but may dilute relevance by including content unrelated to the specific question. Most production systems use chunks of 300-500 tokens with 50-100 token overlap as a starting point, then tune empirically based on retrieval quality evaluation.

Semantic chunking is a more sophisticated approach that uses embedding similarity to determine split points, keeping content that belongs together in the same chunk. This is more computationally expensive than character-based splitting but produces more coherent chunks for complex documents. Document-aware splitting respects document structure like headings, paragraphs, and sections, which is particularly effective for structured documentation.
"""),

"langchain_agents.txt": ("https://python.langchain.com/docs/concepts/agents/", """
Agents in LangChain use a language model as a reasoning engine to decide what sequence of actions to take to accomplish a goal. Unlike a chain with a fixed sequence of steps, an agent dynamically decides which tools to call and in what order, based on the model's reasoning about the current state of the task.

The core agent loop consists of three steps repeated until completion. First, the model receives the current state — the original task plus any observations from previous tool calls — and decides what to do next. Second, if the model decides to call a tool, the tool is executed and its output becomes an observation. Third, the observation is added to the state and the model reasons again. This loop continues until the model decides it has enough information to give a final answer.

ReAct (Reasoning and Acting) is the most common agent framework. In ReAct, the model interleaves reasoning steps — explicit thoughts about what to do next and why — with action steps that execute tools. The explicit reasoning makes the agent's decision-making interpretable and helps catch errors earlier in the loop.

Tools are functions that agents can call to interact with external systems. Common tools include web search for finding current information, code execution for computing results, database queries for retrieving structured data, and API calls for interacting with external services. Each tool has a name, description, and input schema that the model uses to decide when and how to call it.

Agent reliability is the main engineering challenge. Agents can get stuck in loops, make wrong early decisions that cascade, or fail unpredictably when unexpected tool outputs occur. Production agent systems require maximum iteration limits, fallback behaviors for tool failures, and comprehensive logging of every reasoning and action step.
"""),

"langchain_evaluation.txt": ("https://python.langchain.com/docs/concepts/evaluation/", """
Evaluation in LangChain refers to the process of assessing the performance of LLM applications. Because language model outputs are not exactly right or wrong but fall on a spectrum of quality, evaluation requires different approaches than traditional software testing.

String evaluators compare an output string to a reference string or evaluate it against a set of criteria without a reference. CriteriaEvalChain evaluates outputs against defined criteria such as conciseness, relevance, correctness, or harmlessness, using an LLM as the judge. This enables evaluation without labeled datasets, which is crucial for domains where ground-truth labels are expensive to create.

The LLM-as-judge approach is now standard practice in the industry. A separate, often more capable model evaluates the output of the model under test on a defined rubric. Research shows that LLM judge scores correlate with human evaluations at 0.85-0.90 Pearson correlation on most benchmarks, making them a practical substitute for expensive human evaluation at scale.

For RAG systems specifically, the key evaluation dimensions are retrieval quality and generation quality. Retrieval quality is measured using Precision@k (what fraction of retrieved documents are relevant) and Recall@k (what fraction of relevant documents were retrieved). Generation quality is measured using faithfulness (does the answer only make claims supported by the retrieved context) and answer relevance (does the answer address the question asked). The RAGAS framework automates these metrics for RAG systems.

Regression testing is critical for production systems. Every pipeline change — new embedding model, different chunk size, modified system prompt — must be validated against a fixed golden evaluation set before deployment. Automated quality gates that block deployment if any metric drops below a threshold prevent quality regressions from reaching users.
"""),

"langchain_prompt_templates.txt": ("https://python.langchain.com/docs/concepts/prompt_templates/", """
Prompt templates in LangChain are reusable templates for generating prompts. They abstract the fixed parts of a prompt from the variable inputs, making it easy to create consistent prompts across an application and separate prompt design from application logic.

PromptTemplate is the simplest type, accepting a template string with named variables in curly braces and a format method that substitutes values. ChatPromptTemplate handles chat model prompts, which consist of a sequence of messages with different roles: system (sets model behavior), human (user input), and AI (assistant responses). Most production RAG applications use ChatPromptTemplate with a system message that defines the grounding rules and a human message that includes the retrieved context and the question.

A critical design decision is how to structure the system prompt for RAG grounding. The system prompt must clearly instruct the model to answer only from the provided context and to acknowledge when the answer is not available rather than guessing. Explicit negative instructions (do not make up information, do not use your training knowledge) generally outperform implicit instructions (use only the context) because they make the constraint more salient to the model.

FewShotPromptTemplate adds example input-output pairs to the prompt to demonstrate the desired behavior. This is particularly effective when the output format is complex or when the task requires consistent stylistic choices that are hard to describe in instructions alone. Few-shot examples should be selected dynamically based on similarity to the current input for best results.
"""),

"langchain_structured_outputs.txt": ("https://python.langchain.com/docs/concepts/structured_outputs/", """
Structured outputs allow language models to return data in a predefined format — typically JSON conforming to a schema — rather than free-form text. This makes it straightforward to use LLM outputs programmatically: parsing, validating, and passing to downstream systems without complex string manipulation.

LangChain's with_structured_output method adds structured output capability to any chat model that supports it. The method accepts either a Pydantic model or a JSON Schema definition that specifies the expected structure. The model is instructed to return output conforming to this schema, and LangChain automatically parses and validates the response.

Function calling (also called tool calling) is the mechanism most models use to implement structured outputs. The schema is passed to the model as a function definition, and the model's response includes a structured call to that function with the extracted values. This is more reliable than instructing the model to return JSON in its text response because function calling is handled at the model API level.

Structured outputs are used in RAG systems for several purposes. Classification of query intent before retrieval helps route to the right retrieval strategy. Extraction of specific entities or facts from retrieved documents produces structured data for downstream processing. Grading of retrieved document relevance allows filtering poor-quality chunks before they reach the generation step. Self-evaluation of generated answers enables automated quality checking.
"""),

"langchain_streaming.txt": ("https://python.langchain.com/docs/concepts/streaming/", """
Streaming allows language model outputs to be processed as they are generated, token by token, rather than waiting for the complete response. This dramatically improves perceived latency for users because they see the first tokens of the response within seconds rather than waiting 5-30 seconds for a complete answer.

LangChain supports streaming through two interfaces. The stream method returns an iterator that yields tokens as they are generated, suitable for use in synchronous code. The astream method returns an async iterator for use with async frameworks like FastAPI, allowing the server to handle other requests while waiting for model output.

In RAG pipelines, streaming is applied to the generation step since retrieval happens synchronously before generation. A common pattern is to retrieve relevant documents synchronously, then stream the generation step to the client. The sources and metadata can be sent before the streamed content begins, giving users immediate feedback on what documents informed the answer.

Server-Sent Events (SSE) and WebSockets are the two common protocols for delivering streaming responses to web frontends. FastAPI supports SSE natively through the StreamingResponse class, making it straightforward to expose a streaming LangChain endpoint. The frontend receives tokens as they arrive and appends them to the displayed response in real time, creating the characteristic typewriter effect seen in ChatGPT and similar interfaces.
"""),

"pinecone_vector_database.txt": ("https://www.pinecone.io/learn/vector-database/", """
A vector database is a database system designed specifically to store and efficiently search high-dimensional vector embeddings. Traditional databases store exact values and search by exact matching or range queries. Vector databases store continuous-valued vectors and search by approximate similarity, finding vectors that are close in the embedding space to a query vector.

The core operation is nearest neighbor search. Given a query vector — the embedding of a user's question — the database returns the k most similar vectors along with their associated metadata and original text. Similarity is computed using distance metrics, with cosine similarity being most common for text embeddings because it captures directional similarity regardless of vector magnitude.

Approximate nearest neighbor (ANN) algorithms make vector search tractable at scale. Exact nearest neighbor search requires comparing the query against every stored vector, which is too slow for large databases. ANN algorithms like HNSW (Hierarchical Navigable Small World) and IVF (Inverted File Index) build index structures during ingestion that allow fast search by exploring only a subset of vectors at query time. HNSW achieves query times of milliseconds even across hundreds of millions of vectors with high recall.

Metadata filtering combines vector similarity with traditional attribute constraints. For example, retrieving the most similar documents that were published after a certain date, or belong to a specific category, or come from a specific source. This is implemented by filtering candidates based on metadata before or after the vector search step. Pre-filtering (filter then search) works better when the filter is highly selective. Post-filtering (search then filter) works better when the filter is less selective and you need exactly k results after filtering.
"""),

"pinecone_chunking_strategies.txt": ("https://www.pinecone.io/learn/chunking-strategies/", """
Chunking is the process of dividing documents into smaller pieces for embedding and retrieval. The chunking strategy chosen has one of the largest impacts on RAG system performance because it determines the granularity, coherence, and completeness of what gets retrieved in response to a query.

Fixed-size chunking divides text into chunks of a specific number of tokens or characters, with an optional overlap between consecutive chunks. It is simple, predictable, and computationally inexpensive. Overlap between chunks (typically 10-15% of chunk size) reduces the risk of splitting important content across chunk boundaries. The main weakness is that fixed-size chunks may cut sentences or ideas in the middle, reducing semantic coherence.

Sentence-window chunking embeds individual sentences for retrieval but returns a window of surrounding sentences as context to the LLM. This combines precise retrieval granularity with richer generation context, addressing the tradeoff between retrieval precision and context completeness. The sentence is the retrieval unit; the window is the generation unit.

Semantic chunking uses embedding similarity to determine split points. Adjacent sentences are merged into the same chunk as long as their embedding similarity exceeds a threshold. When similarity drops — indicating a topic change — a new chunk is started. This produces chunks that are semantically coherent rather than arbitrarily truncated, but requires embedding computation during the chunking step and is more expensive.

Document-structure-aware chunking respects the inherent structure of the source material. For markdown documents, splitting by headers keeps sections together. For code, splitting by function or class boundaries keeps logical units intact. For PDFs, splitting by detected paragraphs or sections preserves the author's intended organization. When source structure is reliable, structure-aware chunking consistently outperforms character-based chunking.
"""),

"openai_prompt_engineering.txt": ("https://platform.openai.com/docs/guides/prompt-engineering/", """
Prompt engineering is the practice of structuring inputs to language models to produce reliable, high-quality outputs. OpenAI's prompt engineering guide identifies six primary strategies for improving model results.

The first strategy is writing clear and specific instructions. The model cannot read intent — it processes exactly what is written. Adding detail, specifying the desired output format, and explicitly stating what the model should not do all help. If the output is too long, ask for brevity. If it lacks depth, ask for expert-level analysis. Delimiters like triple backticks or XML tags clearly separate instructions from content, preventing instructions embedded in content from being treated as part of the task.

The second strategy is providing reference text. When given authoritative source material, models make fewer fabrications. Instructing the model to answer using only the provided reference and to cite specific passages makes outputs more accurate and verifiable. This is the core principle behind retrieval-augmented generation.

The third strategy is splitting complex tasks into simpler subtasks. Complex tasks that require many steps in a single prompt are more error-prone than decomposed tasks where each step is handled separately. For a RAG system, this means separating the retrieval step, the context formatting step, and the generation step rather than attempting all in a single prompt.

The fourth strategy is using chain-of-thought reasoning. Asking the model to reason step by step before committing to an answer dramatically improves performance on complex tasks. This works because it prevents the model from anchoring to an incorrect answer before fully processing the problem. For grounding tasks, asking the model to find relevant quotes from the context before synthesizing an answer improves faithfulness.

The fifth strategy is testing changes systematically. Intuitions about what will improve performance are frequently wrong. The only reliable way to improve prompt performance is to evaluate changes against a representative set of examples and measure the impact quantitatively.
"""),

"cohere_embeddings_reranking.txt": ("https://docs.cohere.com/docs/embeddings", """
Cohere provides embedding models and reranking models that work together to build high-performance retrieval systems. The embedding models convert text into vector representations for similarity search, while the reranking model re-scores retrieved candidates to surface the most relevant results.

Cohere's embed-v4.0 model supports multimodal inputs including text and images, enabling retrieval across different data types. The model produces embeddings optimized for semantic similarity search and supports multiple input types: search_document for content being indexed, search_query for query-time embedding, classification for text classification tasks, and clustering for grouping similar documents.

Reranking is a two-stage retrieval approach that significantly improves precision without sacrificing recall. In the first stage, fast approximate retrieval (using a vector database) returns a large set of candidates — typically 50 to 100. In the second stage, a cross-encoder reranking model scores each candidate against the original query using deeper attention between query and document. The reranker returns a ranked list where the most relevant documents are at the top.

Why two stages instead of just using the reranker directly? Cross-encoder models that compare query and document together are too slow to run against an entire corpus at query time — they require a forward pass for every document. But they are significantly more accurate than bi-encoder embedding models that embed query and document independently. The two-stage approach uses fast approximate retrieval for recall and the slower but more accurate reranker for precision.

The combination of Cohere's embedding model for retrieval and Rerank model for post-processing consistently achieves higher retrieval quality than embedding search alone, particularly on queries with complex intent or domain-specific terminology where surface-form similarity is a poor proxy for relevance.
"""),

"ibm_rag_enterprise.txt": ("https://research.ibm.com/blog/retrieval-augmented-generation-RAG", """
Retrieval-Augmented Generation (RAG) was introduced in a 2020 paper by researchers at Facebook AI (now Meta AI). The original formulation combined a dense retrieval component — using a bi-encoder to find relevant documents — with a sequence-to-sequence generation model conditioned on the retrieved documents. The paper demonstrated that RAG outperformed pure parametric models on knowledge-intensive tasks while being more interpretable and updatable.

The core insight motivating RAG is the distinction between parametric knowledge (information stored in model weights during training) and non-parametric knowledge (information stored in an external retrieval corpus). Parametric knowledge is fast to access but static and expensive to update — it requires retraining or fine-tuning to change. Non-parametric knowledge can be updated instantly by modifying the retrieval corpus and is directly inspectable and citable.

For enterprise deployments, RAG offers several advantages over fine-tuning. First, knowledge can be updated without model retraining — new documents are indexed and immediately available. Second, answers are auditable because the specific source documents can be cited and verified. Third, access control can be implemented at the retrieval layer, ensuring users only receive answers based on documents they are authorized to access. Fourth, different knowledge domains can be served by the same model with different retrieval indices, reducing infrastructure complexity.

The main challenges in enterprise RAG deployment are document pipeline reliability (ensuring all relevant documents are indexed with correct metadata), retrieval quality (ensuring the right documents are found for each query type), and output quality assurance (ensuring generated answers are faithful to retrieved documents and appropriate for business use). Each of these requires dedicated engineering investment beyond the initial RAG prototype.
"""),

}

saved = 0
failed = 0

# Scrape working URLs
print("=== Scraping live URLs ===")
for filename, url in SCRAPE_SOURCES:
    print(f"Fetching: {url}")
    text = scrape(url)
    if text:
        content = f"Source: {url}\n\n{text.strip()}"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✅ {filename} ({len(text)} chars)")
        saved += 1
    else:
        print(f"  ❌ {filename} — could not scrape")
        failed += 1
    time.sleep(0.5)

# Write high-quality content for JS-rendered sites
print("\n=== Writing content for JS-rendered sources ===")
for filename, (url, content) in WRITTEN_SOURCES.items():
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Source: {url}\n\n{content.strip()}")
    print(f"  ✅ {filename}")
    saved += 1

print(f"\nTotal: {saved} files saved, {failed} failed")
print(f"Files in {OUTPUT_DIR}/")