import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

PDF_PATH = (
    BASE_DIR
    / "data"
    / "bhagavad-gita.pdf"
)

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
)

OLLAMA_LLM = os.getenv(
    "OLLAMA_LLM",
    "llama3.2:1b",
)

OLLAMA_EMBED_MODEL = os.getenv(
    "OLLAMA_EMBED_MODEL",
    "nomic-embed-text",
)


POSTGRES_HOST = os.getenv(
    "POSTGRES_HOST",
    "localhost",
)

POSTGRES_PORT = int(
    os.getenv(
        "POSTGRES_PORT",
        "5432",
    )
)

POSTGRES_USER = os.getenv(
    "POSTGRES_USER",
    "raguser",
)

POSTGRES_PASSWORD = os.getenv(
    "POSTGRES_PASSWORD",
    "ragpassword",
)

POSTGRES_DB = os.getenv(
    "POSTGRES_DB",
    "ragdb",
)

PGVECTOR_TABLE = os.getenv(
    "PGVECTOR_TABLE",
    "gita_vectors",
)


TOP_K = int(
    os.getenv(
        "TOP_K",
        "2",
    )
)

CONTEXT_WINDOW = int(
    os.getenv(
        "CONTEXT_WINDOW",
        "2048",
    )
)

APP_NAME = "Bhagavad Gita RAG"

DEBUG = os.getenv(
    "DEBUG",
    "false",
).lower() == "true"


def validate_config():

    print("\n" + "=" * 60)
    print("CONFIGURATION")
    print("=" * 60)

    if PDF_PATH.exists():
        print("PDF status   : OK")
    else:
        print(
            f"PDF status   : NOT FOUND"
        )
        print(
            f"Expected at  : {PDF_PATH}"
        )

    print("=" * 60)

if __name__ == "__main__":

    validate_config()