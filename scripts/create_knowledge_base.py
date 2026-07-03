"""
create_knowledge_base.py — creates a rich AI engineering knowledge base
covering topics people actually search for in LangChain/LLM interviews
"""
import os

OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

docs = {
"rag_fundamentals.txt": """
Retrieval-Augmented Generation (RAG) is an AI framework that combines information retrieval with text generation. Instead of relying solely on an LLM's training data, RAG systems first retrieve relevant documents from an external knowledge base, then use those documents as context for generating accurate, grounded responses.

The core RAG pipeline has five stages. First, document ingestion: raw documents are loaded and split into smaller chunks using text splitters. Second, embedding: each chunk is converted into a vector representation using an embedding model that captures semantic meaning. Third, storage: these vectors are stored in a vector database like ChromaDB, Pinecone, or FAISS that supports fast similarity search. Fourth, retrieval: when a user asks a question, the query is embedded and the most semantically similar chunks are retrieved from the vector store. Fifth, generation: the retrieved chunks are passed as context to an LLM, which generates a grounded answer.

RAG solves several key problems with pure LLM generation. LLMs have a knowledge cutoff and cannot access real-time or proprietary information. RAG allows LLMs to answer questions about documents they were never trained on. RAG also reduces hallucination by forcing the model to ground its answers in retrieved facts rather than relying on potentially incorrect memorized knowledge.

The main variations of RAG include naive RAG (basic retrieve-then-generate), advanced RAG (with query rewriting, reranking, and hybrid search), and modular RAG (with routing, fusion, and adaptive retrieval). Each variation trades off complexity for accuracy and latency.

Common failure modes in RAG systems include retrieval failures (the right document is not retrieved due to vocabulary mismatch or poor chunking), generation failures (the LLM ignores or misrepresents the retrieved context), and context window overflow (too many retrieved chunks exceed the LLM's context limit).
""",

"vector_databases.txt": """
Vector databases are specialized databases designed to store and efficiently search high-dimensional vector embeddings. Unlike traditional relational databases that search by exact matching, vector databases use approximate nearest neighbor algorithms to find vectors that are semantically similar to a query vector.

The most common similarity metrics used in vector databases are cosine similarity, which measures the angle between vectors regardless of their magnitude and is best for text embeddings, and Euclidean distance, which measures the straight-line distance between vectors. For normalized vectors, cosine similarity and dot product produce equivalent rankings.

Popular vector databases include ChromaDB, an open-source local-first database ideal for development and small-to-medium scale applications. Pinecone is a fully managed cloud vector database that scales to billions of vectors. FAISS (Facebook AI Similarity Search) is a library optimized for fast in-memory similarity search. Weaviate and Qdrant are open-source vector databases that combine vector search with traditional filtering capabilities.

Vector databases support two types of search: dense retrieval using embedding vectors, and sparse retrieval using keyword-based approaches like BM25. Hybrid search combines both dense and sparse retrieval to get the benefits of semantic understanding and exact keyword matching. This is particularly useful when queries contain specific technical terms or proper nouns that semantic search might handle poorly.

Key concepts in vector databases include indexing algorithms like HNSW (Hierarchical Navigable Small World) that allow approximate nearest neighbor search in logarithmic time, metadata filtering that allows combining vector similarity with traditional attribute filters, and namespace or collection isolation for separating different knowledge bases within the same database.
""",

"embeddings_explained.txt": """
Embeddings are dense numerical vector representations of text (or other data) that capture semantic meaning. Two pieces of text with similar meanings will have embedding vectors that are close together in the high-dimensional vector space, even if they use completely different words.

How embeddings are created: an embedding model (usually a transformer neural network) processes input text and outputs a fixed-length vector, typically between 384 and 1536 dimensions depending on the model. The model is trained on massive text datasets to learn that similar contexts produce similar vectors. For example, "overfitting" and "memorizing training data" would be close in embedding space because they appear in similar contexts across training documents.

Popular embedding models include OpenAI's text-embedding-3-small and text-embedding-3-large, which are high quality but require API calls. Sentence-transformers like all-MiniLM-L6-v2 are free, open-source models that run locally and are excellent for most use cases. Jina AI provides free API-based embeddings that are competitive with commercial options. Cohere's embedding models are popular for multilingual applications.

The dimensionality of embeddings represents a tradeoff: higher dimensional embeddings capture more nuance but require more storage and computation. The embedding dimension must match between the model used to build the index and the model used to embed queries at search time — mixing models from different providers or of different sizes will produce incorrect results.

Embedding drift is an important production concern: if you switch embedding models, all previously embedded documents must be re-embedded and the vector index must be rebuilt from scratch, since vectors from different models are not comparable.
""",

"chunking_strategies.txt": """
Text chunking is the process of splitting large documents into smaller pieces before embedding and indexing. Chunking strategy significantly impacts RAG system quality because it determines what context is retrieved and how much semantic meaning is preserved in each piece.

Fixed-size chunking splits text into chunks of a fixed number of tokens or characters, with an optional overlap between consecutive chunks. Chunk size controls the granularity of retrieval: small chunks (100-200 tokens) are precise but may lack context, while large chunks (1000+ tokens) preserve context but may dilute relevance. Overlap (typically 10-20% of chunk size) prevents important information from being split across chunk boundaries.

Semantic chunking splits text based on meaning rather than fixed sizes, keeping related sentences together. This produces more coherent chunks but is more complex to implement. Sentence-level chunking treats each sentence as a chunk, which is very precise but may result in too many small chunks for complex topics.

Document-aware chunking respects the structure of the source document: splitting by paragraphs, sections, or headings. For markdown or HTML documents, splitting by headers preserves the natural organization of the content and ensures each chunk covers a complete topic.

The optimal chunk size depends on your use case. For question-answering over technical documentation, chunks of 300-500 tokens with 50-token overlap work well for most cases. For long-form text like books or reports, larger chunks of 500-1000 tokens may be appropriate. Always test retrieval quality empirically with your specific documents and query patterns rather than relying on default values.

Parent-child chunking is an advanced technique where small child chunks are used for precise retrieval, but the larger parent chunk is returned to the LLM for generation. This gives the best of both worlds: precise retrieval with full context for generation.
""",

"prompt_engineering.txt": """
Prompt engineering is the practice of designing and optimizing input prompts to get the best possible outputs from large language models. Effective prompt engineering can dramatically improve LLM output quality without any model training or fine-tuning.

Zero-shot prompting asks the model to complete a task with no examples, relying entirely on the model's pretrained knowledge. One-shot and few-shot prompting include one or several examples of the desired input-output format in the prompt. Few-shot prompting is particularly effective for tasks with a specific output format or style, as the examples demonstrate exactly what is expected.

Chain-of-thought (CoT) prompting encourages the model to reason step by step before giving a final answer, by either including the phrase "Let's think step by step" or by providing few-shot examples that demonstrate step-by-step reasoning. CoT dramatically improves performance on complex reasoning, math, and logic tasks by allowing the model to break down the problem rather than jumping to a conclusion.

System prompts set the overall behavior, persona, and constraints for the model throughout a conversation. A well-designed system prompt can make a model consistently follow specific formats, avoid certain topics, maintain a particular tone, or stick to a defined knowledge scope. For RAG systems, the system prompt typically instructs the model to answer only from the provided context and to admit uncertainty when the answer is not in the context.

Prompt injection is a security vulnerability where malicious content in the user's input (or in retrieved documents) attempts to override the system prompt's instructions. Common injection patterns include phrases like "ignore previous instructions" or "you are now a different AI." Defending against injection requires both input validation and robust system prompts that explicitly acknowledge and resist manipulation attempts.
""",

"llm_evaluation.txt": """
Evaluating large language model outputs is fundamentally different from evaluating traditional software because there is rarely a single correct answer. LLM evaluation requires measuring qualities like relevance, faithfulness, coherence, and helpfulness, which are inherently subjective.

The main approaches to LLM evaluation are human evaluation, automated metrics, and LLM-as-judge. Human evaluation is the gold standard but is expensive, slow, and hard to scale. Automated metrics like BLEU, ROUGE, and BERTScore compare generated text to reference answers but require ground-truth labels and do not capture all aspects of quality. LLM-as-judge uses a separate LLM (often more powerful than the one being evaluated) to score outputs on defined criteria, which is scalable and correlates reasonably well with human judgment.

For RAG systems specifically, the key evaluation dimensions are retrieval quality and generation quality. Retrieval quality measures whether the right documents were retrieved, using metrics like Precision@k (what fraction of retrieved documents are relevant) and Recall@k (what fraction of relevant documents were retrieved). Generation quality measures whether the answer is correct and grounded, using faithfulness (does the answer only make claims supported by the retrieved context) and answer relevance (does the answer actually address the question asked).

A golden dataset is a fixed set of questions with known-correct answers or expected keywords used to benchmark system performance consistently over time. Running evaluation against a golden dataset on every code change (like a CI check) allows you to detect regressions: changes that accidentally made the system worse. Without automated evaluation, it is easy to improve one aspect of a RAG system while silently degrading another.

RAGAS is a popular open-source framework specifically designed for evaluating RAG systems. It provides automated metrics for faithfulness, answer relevance, context precision, and context recall using LLM-based scoring. The key insight behind frameworks like RAGAS is that LLM-based evaluation, while imperfect, is far more scalable than human evaluation and produces actionable scores that can be tracked over time.
""",

"guardrails_and_safety.txt": """
AI guardrails are safety mechanisms that validate inputs and outputs of AI systems to prevent misuse, ensure quality, and protect against security vulnerabilities. In production RAG systems, guardrails operate at multiple stages of the pipeline.

Input guardrails validate user queries before they reach the retrieval or generation stages. They check for prompt injection attempts (malicious instructions designed to override the system's behavior), inappropriate content, personally identifiable information in queries, and other policy violations. A two-layer approach is common: a fast pattern-matching layer catches known attack patterns immediately, followed by an LLM-based classifier that can detect novel injection attempts that pattern matching misses.

Prompt injection is one of the most significant security risks for LLM-based applications and is listed as the number one risk in the OWASP LLM Top 10. Direct prompt injection comes from the user's input. Indirect prompt injection comes from content in retrieved documents that contains hidden instructions, such as a malicious webpage that has been indexed into the knowledge base.

Output guardrails validate generated responses before they are returned to the user. They check for hallucinations (claims not supported by retrieved context), sensitive information leakage (API keys, passwords, PII that may have been in source documents), harmful content, and policy violations. Faithfulness checking using LLM-as-judge determines whether each claim in the generated response is actually supported by the retrieved context.

Defense in depth is the principle of having multiple independent security layers rather than relying on a single mechanism. For AI systems, this means combining prompt engineering (instruct the model to behave safely), input validation (filter malicious inputs before they reach the model), output validation (check outputs before returning them to users), and monitoring (log everything so attacks can be detected and analyzed). No single layer is perfect, but multiple layers working together provide robust protection.
""",

"agents_and_tools.txt": """
An AI agent is a system where a large language model is used as a reasoning engine that can decide what actions to take, execute those actions using tools, observe the results, and iterate until it completes a goal. Unlike a simple question-answering system, an agent can break down complex multi-step problems and adapt its approach based on intermediate results.

The ReAct (Reasoning and Acting) pattern is the most common agent framework. In ReAct, the LLM alternates between reasoning (thinking about what to do next) and acting (calling a tool or taking an action). The loop continues until the model determines it has enough information to provide a final answer. Each reasoning step is visible, which makes agents more interpretable than single-shot generation.

Tools are functions that an agent can call to interact with the outside world. Common tools include web search (fetching current information), code execution (running Python to compute results), database queries (looking up structured data), API calls (interacting with external services), and file operations (reading or writing files). The LLM decides which tool to call based on the task, and the tool's output becomes part of the context for the next reasoning step.

The main challenges with agents are reliability and cost. Agents can get stuck in loops, make wrong decisions early that cascade into larger errors, and accumulate large context windows across many tool calls. Agents are also significantly more expensive than single-shot generation because they make multiple LLM calls per user request. For production use cases, it is important to set maximum iteration limits, implement fallback behaviors, and log every step of the agent's decision-making process for debugging.

LangGraph is a framework built on top of LangChain specifically designed for building reliable, stateful agent workflows. It represents agent behavior as a directed graph where nodes are processing steps and edges are transitions between steps. LangGraph makes it easier to implement complex agent patterns like human-in-the-loop approval, parallel tool execution, and conditional routing between different agent behaviors.
""",

"fine_tuning_vs_rag.txt": """
Fine-tuning and Retrieval-Augmented Generation (RAG) are two complementary approaches for adapting large language models to specific domains or tasks. Understanding when to use each approach, and how to combine them, is a key skill for production AI engineering.

Fine-tuning involves training a pre-trained model on a domain-specific dataset to adjust its weights. After fine-tuning, the model's knowledge and style are permanently changed. Fine-tuning is effective for teaching the model a specific output format or writing style, improving performance on a narrow task where many examples exist, and reducing inference-time context length by baking knowledge into weights rather than passing it in the prompt.

RAG retrieves relevant information at inference time and passes it as context, without modifying the model's weights. RAG is more appropriate when the knowledge base changes frequently, when you need to cite sources, when you have a large diverse knowledge base that cannot fit into a training dataset, or when you want to control what information the model uses on a per-query basis.

The key tradeoff is that fine-tuning is better for style and format adaptation but requires expensive retraining whenever knowledge changes. RAG is better for factual question-answering over dynamic knowledge bases but requires maintaining an external index and increases inference latency due to retrieval.

In practice, many production systems combine both: fine-tuning for style, persona, and instruction-following behavior, combined with RAG for grounding responses in up-to-date, domain-specific facts. For example, a customer support system might fine-tune a model to respond in the company's specific tone and format, then use RAG to ensure answers are based on the current product documentation rather than the model's training data.
""",

"production_ai_systems.txt": """
Building a production AI system is fundamentally different from building a prototype or demo. Production systems must handle real users, varying inputs, service failures, cost constraints, and changing requirements over time.

Observability is the ability to understand what your system is doing at runtime. For AI systems, this means logging every request and response, recording retrieval results and scores, tracking latency at each stage of the pipeline, and monitoring for anomalies like unusual block rates or declining quality scores. Without comprehensive logging, debugging production issues becomes extremely difficult because AI system failures are often subtle and non-deterministic.

Latency management is critical for user experience. A typical RAG pipeline involves embedding the query, vector search, LLM generation, and sometimes additional steps like reranking or faithfulness checking. Each step adds latency. Common optimizations include caching embeddings for repeated queries, using faster but slightly less accurate embedding models, streaming LLM responses so users see text appearing immediately rather than waiting for the full response, and running non-blocking steps like logging in the background rather than in the critical path.

Cost management is essential at scale. LLM API calls are the dominant cost in most RAG systems. Techniques for reducing cost include using smaller, cheaper models for tasks that do not require full capability (such as classification or simple extraction), implementing semantic caching to avoid re-generating responses for similar queries, and batching requests where real-time response is not required.

Testing AI systems requires different approaches than testing traditional software. Unit tests can verify that guardrails block specific known-bad inputs. Integration tests can verify that the full pipeline produces correct outputs for a golden dataset. But AI systems also exhibit emergent failures that only appear with specific input patterns or at scale. Running a diverse evaluation set regularly and tracking metrics over time is the most reliable way to catch regressions before they affect users.
"""
}

saved = 0
for filename, content in docs.items():
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"✅ Created {filename} ({len(content)} chars)")
    saved += 1

print(f"\nDone: {saved} knowledge base files created in {OUTPUT_DIR}/")