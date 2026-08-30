import os
from pathlib import Path

from dotenv import load_dotenv

from docling.document_converter import DocumentConverter

from llama_index.core import (
    Document,
    Settings,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.core.node_parser import SentenceSplitter

from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.postgres import PGVectorStore


load_dotenv()

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)

OLLAMA_LLM = os.getenv(
    "OLLAMA_LLM",
    "llama3.2:1b"
)

OLLAMA_EMBED_MODEL = os.getenv(
    "OLLAMA_EMBED_MODEL",
    "nomic-embed-text"
)

POSTGRES_HOST = os.getenv(
    "POSTGRES_HOST",
    "localhost"
)

POSTGRES_PORT = int(
    os.getenv("POSTGRES_PORT", "5432")
)

POSTGRES_USER = os.getenv(
    "POSTGRES_USER",
    "raguser"
)

POSTGRES_PASSWORD = os.getenv(
    "POSTGRES_PASSWORD",
    "ragpassword"
)

POSTGRES_DB = os.getenv(
    "POSTGRES_DB",
    "ragdb"
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent

PDF_PATH = PROJECT_ROOT / "data" / "bhagavad-gita.pdf"

if not PDF_PATH.exists():
    raise FileNotFoundError(
        f"PDF not found: {PDF_PATH}"
    )


print("=" * 60)
print("AGENTIC RAG SYSTEM")
print("=" * 60)
print("=" * 60)

llm = Ollama(
    model=OLLAMA_LLM,
    base_url=OLLAMA_BASE_URL,
    request_timeout=180.0,
    context_window=2048,
    additional_kwargs={
        "num_ctx": 2048
    },
)


embed_model = OllamaEmbedding(
    model_name=OLLAMA_EMBED_MODEL,
    base_url=OLLAMA_BASE_URL,
)


Settings.llm = llm
Settings.embed_model = embed_model

converter = DocumentConverter()

result = converter.convert(
    str(PDF_PATH)
)

markdown = result.document.export_to_markdown()
print(f"Characters extracted: {len(markdown)}")


document = Document(
    text=markdown,
    metadata={
        "source": PDF_PATH.name,
        "file_path": str(PDF_PATH),
    },
)

splitter = SentenceSplitter(
    chunk_size=500,
    chunk_overlap=80,
)

nodes = splitter.get_nodes_from_documents(
    [document]
)

print(f"Total chunks created: {len(nodes)}")

vector_store = PGVectorStore.from_params(
    database=POSTGRES_DB,
    host=POSTGRES_HOST,
    password=POSTGRES_PASSWORD,
    port=POSTGRES_PORT,
    user=POSTGRES_USER,
    table_name="gita_rag",
    embed_dim=768,
)

storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)

index = VectorStoreIndex(
    nodes,
    storage_context=storage_context,
)

query_engine = index.as_query_engine(
    similarity_top_k=2,
    response_mode="compact",
)


print("\n" + "=" * 60)
print("RAG SYSTEM READY")
print("=" * 60)

print("Ask questions about the Bhagavad Gita.")
print("Type 'exit' to stop.")
print("=" * 60)


while True:

    question = input("\nAsk a question about the Bhagavad Gita: ")

    if question.lower().strip() in {
        "exit",
        "quit",
    }:
        print("Goodbye!")
        break

    if not question.strip():
        continue

    try:

        print("\nSearching document...")

        response = query_engine.query(question)

        print("\nAnswer:")
        print("-" * 60)
        print(response)
        print("-" * 60)

    except Exception as e:

        print("\nERROR while generating answer:")
        print(e)
        print("\nPossible causes:")
        print("1. Ollama model stopped.")
        print("2. Not enough RAM.")
        print("3. PostgreSQL/PGVector is not running.")