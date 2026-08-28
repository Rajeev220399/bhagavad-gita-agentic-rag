# bhagavad-gita-agentic-rag
Production-grade, 100% open-source local Agentic RAG system built with CrewAI, LlamaIndex, Docling, Ollama, and PGVector for domain-specific document intelligence.
## 📌 Project Description

This project is a **100% open-source, fully local Agentic Retrieval-Augmented Generation (RAG) system** engineered for private, domain-specific document intelligence. Built around the Bhagavad Gita as a domain test case, the architecture decouples document processing, retrieval, multi-agent orchestration, and client API layers into a modular system.

### 🌟 Core Architecture & Engineering Highlights

* **Document Parsing & Extraction:** Integrated **Docling** for structured, layout-aware PDF conversion[cite: 5, 6].
* **Vector Storage & Indexing:** Powered by **LlamaIndex** paired with **PGVector (PostgreSQL)** for persistent, high-dimensional vector search[cite: 6].
* **Agentic Orchestration:** Utilizes **CrewAI** to manage dynamic tool selection, multi-step execution, and agent reasoning paths[cite: 1, 2, 7].
* **Local Inference & Embeddings:** Configured with **Ollama** running open-weight LLMs (`llama3.2:1b`) and embedding models (`nomic-embed-text`) for zero-data-leakage local execution[cite: 4, 6, 9].
* **Citation Management & Source Grounding:** Implemented a custom citation engine tracking chunk metadata, source documents, and text references[cite: 3].
* **Conversation Memory:** Built a stateful conversation memory buffer to retain multi-turn context across agent interactions[cite: 8].
* **FastAPI Backend:** Exposed via containerized REST endpoints (`/ask`, `/health`) with dynamic Pydantic request/response schemas[cite: 2].

---

## 🛠️ Stack Overview

* **Orchestration:** CrewAI[cite: 1, 2, 7]
* **RAG Framework:** LlamaIndex[cite: 2, 6, 9]
* **Parser:** Docling[cite: 5, 6, 9]
* **Vector Database:** PostgreSQL / PGVector[cite: 2, 4, 6, 9]
* **Local LLM Engine:** Ollama[cite: 1, 2, 4, 6, 7, 9]
* **API Framework:** FastAPI & Uvicorn[cite: 2]
