from typing import Any, Dict, List
class CitationManager:
    def __init__(self):
        pass

    def create_citation(
        self,
        node: Any,
        citation_number: int,
    ) -> Dict[str, Any]:

        metadata = getattr(
            node,
            "metadata",
            {}
        ) or {}

        source = metadata.get(
            "source",
            "Unknown source",
        )

        chunk_id = metadata.get(
            "chunk_id",
            "Unknown",
        )

        title = metadata.get(
            "title",
            "Bhagavad Gita",
        )

        document_type = metadata.get(
            "document_type",
            "Document",
        )

        return {
            "citation_number": citation_number,
            "title": title,
            "source": source,
            "chunk_id": chunk_id,
            "document_type": document_type,
        }
    def create_citations(
        self,
        nodes: List[Any],
    ) -> List[Dict[str, Any]]:

        citations = []

        for number, node in enumerate(
            nodes,
            start=1,
        ):

            citation = self.create_citation(
                node=node,
                citation_number=number,
            )

            citations.append(
                citation
            )

        return citations

    def format_citation(
        self,
        citation: Dict[str, Any],
    ) -> str:
        """
        Convert citation dictionary into readable text.
        """

        number = citation.get(
            "citation_number",
            "?",
        )

        title = citation.get(
            "title",
            "Unknown",
        )

        source = citation.get(
            "source",
            "Unknown source",
        )

        chunk_id = citation.get(
            "chunk_id",
            "Unknown",
        )

        return (
            f"[{number}] {title}\n"
            f"    Source: {source}\n"
            f"    Chunk: {chunk_id}"
        )
    def format_citations(
        self,
        citations: List[Dict[str, Any]],
    ) -> str:
        """
        Convert all citations into readable text.
        """

        if not citations:
            return "No sources available."

        formatted = []

        for citation in citations:

            formatted.append(
                self.format_citation(
                    citation
                )
            )

        return "\n\n".join(
            formatted
        )

    def build_sources_section(
        self,
        citations: List[Dict[str, Any]],
    ) -> str:
        """
        Create a complete Sources section.
        """

        if not citations:
            return (
                "\n\nSources:\n"
                "No sources available."
            )

        formatted = self.format_citations(
            citations
        )

        return (
            "\n\n"
            "Sources:\n"
            "--------\n"
            f"{formatted}"
        )
class MockNode:

    def __init__(
        self,
        source: str,
        chunk_id: int,
        title: str,
    ):

        self.metadata = {
            "source": source,
            "chunk_id": chunk_id,
            "title": title,
            "document_type": "PDF",
        }


def main():

    print("=" * 60)
    print("CITATION MANAGER TEST")
    print("=" * 60)

    nodes = [
        MockNode(
            source="bhagavad-gita.pdf",
            chunk_id=25,
            title="Bhagavad Gita",
        ),
        MockNode(
            source="bhagavad-gita.pdf",
            chunk_id=41,
            title="Bhagavad Gita",
        ),
    ]

    manager = CitationManager()

    citations = manager.create_citations(
        nodes
    )

    print(
        f"\nCitations created: "
        f"{len(citations)}"
    )

    print("\nFormatted citations:")
    print("-" * 60)

    print(
        manager.format_citations(
            citations
        )
    )

    print("\nSources section:")
    print("-" * 60)

    print(
        manager.build_sources_section(
            citations
        )
    )

    print("=" * 60)
    print("CITATION TEST SUCCESSFUL")
    print("=" * 60)


if __name__ == "__main__":
    main()