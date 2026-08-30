from typing import List

from llama_index.core import (
    Settings,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.postgres import PGVectorStore

from config import (
    OLLAMA_BASE_URL,
    OLLAMA_EMBED_MODEL,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
    PGVECTOR_TABLE,
)


class VectorStoreManager:
    
    def __init__(self):
        print("\n[VectorStore] Initializing...")

        
        print(
            f"[VectorStore] Embedding model: "
            f"{OLLAMA_EMBED_MODEL}"
        )

        self.embed_model = OllamaEmbedding(
            model_name=OLLAMA_EMBED_MODEL,
            base_url=OLLAMA_BASE_URL,
        )

        Settings.embed_model = self.embed_model

        print(
            "[VectorStore] Connecting to PostgreSQL..."
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

        
        self.storage_context = (
            StorageContext.from_defaults(
                vector_store=self.vector_store
            )
        )

        print(
            "[VectorStore] PostgreSQL + PGVector ready."
        )

    def create_index(
        self,
        nodes: List,
    ) -> VectorStoreIndex:
        
        if not nodes:
            raise ValueError(
                "No document chunks were provided."
            )

        print(
            f"\n[VectorStore] Creating vector index "
            f"from {len(nodes)} chunks..."
        )

        index = VectorStoreIndex(
            nodes,
            storage_context=self.storage_context,
        )

        print(
            "[VectorStore] Vector index created "
            "successfully."
        )

        return index


def main():
    
    print("=" * 60)
    print("VECTOR STORE TEST")
    print("=" * 60)


    from document_processor import DocumentProcessor

    processor = DocumentProcessor()

    nodes = processor.process()

    print(
        f"\n[VectorStore] Received "
        f"{len(nodes)} chunks."
    )

    
    manager = VectorStoreManager()

    index = manager.create_index(nodes)

    if index is not None:
        print("\n" + "=" * 60)
        print("VECTOR STORE TEST SUCCESSFUL")
        print("=" * 60)
        print(
            "Embeddings have been generated and "
            "stored in PostgreSQL + PGVector."
        )
        print("=" * 60)


if __name__ == "__main__":
    main()