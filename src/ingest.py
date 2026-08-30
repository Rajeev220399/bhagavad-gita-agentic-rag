import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from docling.document_converter import DocumentConverter

from llama_index.core import (
    Document,
    Settings,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.core.node_parser import SentenceSplitter

from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.postgres import PGVectorStore

from config import (
    PDF_PATH,
    OLLAMA_BASE_URL,
    OLLAMA_EMBED_MODEL,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
    PGVECTOR_TABLE,
)

EMBED_DIM = 768

CHUNK_SIZE = 500

CHUNK_OVERLAP = 50

embed_model = OllamaEmbedding(
    model_name=OLLAMA_EMBED_MODEL,
    base_url=OLLAMA_BASE_URL,
)

Settings.embed_model = embed_model

print(
    f"Embedding model: {OLLAMA_EMBED_MODEL}"
)


if not PDF_PATH.exists():

    raise FileNotFoundError(
        f"PDF not found:\n{PDF_PATH}"
    )

print(
    f"PDF found: {PDF_PATH}"
)



converter = DocumentConverter()

result = converter.convert(
    str(PDF_PATH)
)

markdown_text = (
    result.document.export_to_markdown()
)

if not markdown_text.strip():

    raise ValueError(
        "Docling extracted no text from the PDF."
    )

print(
    f"Extracted characters: "
    f"{len(markdown_text):,}"
)

document = Document(
    text=markdown_text,
    metadata={
        "source": PDF_PATH.name,
        "title": "Bhagavad Gita",
        "document_type": "PDF",
    },
)

splitter = SentenceSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)

nodes = splitter.get_nodes_from_documents(
    [document]
)

print(
    f"Created chunks: {len(nodes)}"
)


for index, node in enumerate(
    nodes,
    start=1,
):

    node.metadata["source"] = PDF_PATH.name

    node.metadata["title"] = (
        "Bhagavad Gita"
    )

    node.metadata["document_type"] = (
        "PDF"
    )

    node.metadata["chunk_id"] = index

vector_store = PGVectorStore.from_params(
    database=POSTGRES_DB,
    host=POSTGRES_HOST,
    password=POSTGRES_PASSWORD,
    port=POSTGRES_PORT,
    user=POSTGRES_USER,
    table_name=PGVECTOR_TABLE,
    embed_dim=EMBED_DIM,
)


storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)

print("\nCreating embeddings and storing vectors...")

index = VectorStoreIndex(
    nodes,
    storage_context=storage_context,
    embed_model=embed_model,
)

print("\n" + "=" * 60)
print("INGESTION COMPLETE")
print("=" * 60)

print(
    f"PDF       : {PDF_PATH.name}"
)

print(
    f"Chunks    : {len(nodes)}"
)

print(
    f"Vector DB : {PGVECTOR_TABLE}"
)

print(
    "Embeddings: stored in PGVector"
)

print("=" * 60)