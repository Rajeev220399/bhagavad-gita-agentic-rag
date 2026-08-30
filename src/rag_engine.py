from typing import Any, Dict, List

from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.postgres import PGVectorStore

from config import (
    CONTEXT_WINDOW,
    OLLAMA_BASE_URL,
    OLLAMA_EMBED_MODEL,
    OLLAMA_LLM,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
    PGVECTOR_TABLE,
    TOP_K,
)

from memory import ConversationMemory
from citations import CitationManager


class RAGEngine:
   
    def __init__(self):

        print("\n[RAG] Initializing RAG engine...")
        print(
            f"[RAG] Embedding model: "
            f"{OLLAMA_EMBED_MODEL}"
        )

        self.embed_model = OllamaEmbedding(
            model_name=OLLAMA_EMBED_MODEL,
            base_url=OLLAMA_BASE_URL,
        )

        print(
            f"[RAG] LLM: {OLLAMA_LLM}"
        )

        self.llm = Ollama(
            model=OLLAMA_LLM,
            base_url=OLLAMA_BASE_URL,
            request_timeout=180.0,
            context_window=CONTEXT_WINDOW,
            additional_kwargs={
                "num_ctx": CONTEXT_WINDOW
            },
        )

        Settings.llm = self.llm
        Settings.embed_model = self.embed_model

        print(
            "[RAG] Connecting to PostgreSQL + PGVector..."
        )

        self.vector_store = PGVectorStore.from_params(
            database=POSTGRES_DB,
            host=POSTGRES_HOST,
            password=POSTGRES_PASSWORD,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            table_name=PGVECTOR_TABLE,
            embed_dim=768,
        )

        print(
            "[RAG] Loading existing vector index..."
        )

        self.index = VectorStoreIndex.from_vector_store(
            vector_store=self.vector_store,
            embed_model=self.embed_model,
        )

        self.retriever = VectorIndexRetriever(
            index=self.index,
            similarity_top_k=TOP_K,
        )

        self.memory = ConversationMemory(
            max_turns=5
        )

        self.citation_manager = CitationManager()

        print(
            "[RAG] RAG engine ready."
        )

    def retrieve(
        self,
        question: str,
    ) -> List[Any]:

        if not question.strip():
            return []

        print(
            f"\n[RAG] Retrieving top {TOP_K} chunks..."
        )

        nodes = self.retriever.retrieve(
            question
        )

        print(
            f"[RAG] Retrieved {len(nodes)} chunks."
        )

        return nodes

    def build_document_context(
        self,
        nodes: List[Any],
    ) -> str:

        if not nodes:
            return (
                "No relevant document context "
                "was found."
            )

        context_parts = []

        for index, node in enumerate(
            nodes,
            start=1,
        ):

            text = node.get_content()

            metadata = node.metadata or {}

            source = metadata.get(
                "source",
                "unknown",
            )

            chunk_id = metadata.get(
                "chunk_id",
                "unknown",
            )

            context_parts.append(
                f"""
DOCUMENT SOURCE {index}
Source: {source}
Chunk ID: {chunk_id}

{text}
""".strip()
            )

        return "\n\n".join(
            context_parts
        )

    def build_memory_context(self) -> str:

        return (
            self.memory.get_formatted_history()
        )

    def build_prompt(
        self,
        question: str,
        document_context: str,
        conversation_context: str,
    ) -> str:

        prompt = f"""
You are a helpful Bhagavad Gita question-answering
assistant.

PREVIOUS CONVERSATION
=====================
{conversation_context}

DOCUMENT CONTEXT
================
{document_context}

CURRENT QUESTION
================
{question}

ANSWER
======
"""

        return prompt

    def generate_answer(
        self,
        question: str,
        document_context: str,
        conversation_context: str,
    ) -> str:

        prompt = self.build_prompt(
            question=question,
            document_context=document_context,
            conversation_context=conversation_context,
        )

        print(
            "[RAG] Generating answer with Ollama..."
        )

        response = self.llm.complete(
            prompt
        )

        return str(response).strip()

    def query(
        self,
        question: str,
    ) -> Dict[str, Any]:

        if not question.strip():

            return {
                "answer": "Please enter a question.",
                "sources": [],
            }

        nodes = self.retrieve(
            question
        )

        document_context = (
            self.build_document_context(
                nodes
            )
        )

        conversation_context = (
            self.build_memory_context()
        )

        answer = self.generate_answer(
            question=question,
            document_context=document_context,
            conversation_context=conversation_context,
        )

        citations = (
            self.citation_manager.create_citations(
                nodes
            )
        )
        self.memory.add_turn(
            user_message=question,
            assistant_message=answer,
        )

        return {
            "answer": answer,
            "sources": citations,
        }

    def clear_memory(self):

        self.memory.clear()

        print(
            "[RAG] Conversation memory cleared."
        )

    def memory_size(self) -> int:

        return self.memory.size()

def main():

    print("=" * 60)
    print("RAG + MEMORY + CITATIONS")
    print("=" * 60)

    try:

        engine = RAGEngine()

    except Exception as error:

        print("\n[RAG] Initialization failed.")
        print(error)

        return

    print("\nRAG system is ready.")

    print(
        "\nCommands:"
    )

    print(
        "  exit  -> quit"
    )

    print(
        "  clear -> clear conversation memory"
    )

    while True:

        try:

            question = input(
                "\nYou: "
            ).strip()

        except KeyboardInterrupt:

            print(
                "\n\nExiting..."
            )

            break

        except EOFError:

            print(
                "\n\nExiting..."
            )

            break

        if question.lower() in {
            "exit",
            "quit",
        }:

            print(
                "\nGoodbye!"
            )

            break
        if question.lower() == "clear":

            engine.clear_memory()

            continue
        if not question:

            continue
        try:

            result = engine.query(
                question
            )

            print("\n")
            print("=" * 60)
            print("ANSWER")
            print("=" * 60)

            print(
                result["answer"]
            )

            print("\n")
            print("=" * 60)
            print("SOURCES")
            print("=" * 60)

            citations = result.get(
                "sources",
                [],
            )

            if citations:

                print(
                    engine.citation_manager
                    .format_citations(
                        citations
                    )
                )

            else:

                print(
                    "No sources available."
                )

            print("\n")
            print(
                f"Memory turns: "
                f"{engine.memory_size()}"
            )

            print("=" * 60)

        except Exception as error:

            print("\n")
            print("=" * 60)
            print("RAG ERROR")
            print("=" * 60)

            print(error)

            print("=" * 60)


# =============================================================
# ENTRY POINT
# =============================================================

if __name__ == "__main__":
    main()