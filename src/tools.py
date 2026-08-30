import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from crewai.tools import tool

from rag_engine import RAGEngine

_rag_engine = None


def get_rag_engine():
    global _rag_engine

    if _rag_engine is None:
        _rag_engine = RAGEngine()

    return _rag_engine

@tool("search_bhagavad_gita")
def search_bhagavad_gita(question: str) -> str:
    engine = get_rag_engine()

    nodes = engine.retrieve(
        question
    )

    if not nodes:

        return (
            "No relevant information was found "
            "in the Bhagavad Gita document."
        )

    results = []

    for index, node in enumerate(
        nodes,
        start=1,
    ):

        text = node.get_content()

        metadata = node.metadata or {}

        source = metadata.get(
            "source",
            "Unknown source",
        )

        chunk_id = metadata.get(
            "chunk_id",
            "Unknown",
        )

        results.append(
            f"""
SOURCE {index}
File: {source}
Chunk: {chunk_id}

{text}
""".strip()
        )

    return "\n\n".join(
        results
    )


if __name__ == "__main__":

    print("=" * 60)
    print("=" * 60)

    question = input(
        "\nQuestion: "
    ).strip()

    if question:

        result = search_bhagavad_gita.run(
            question
        )

        print("\n")
        print(result)

    print("\n" + "=" * 60)