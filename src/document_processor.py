from pathlib import Path
from typing import List

from docling.document_converter import DocumentConverter
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter

from config import (
    PDF_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

class DocumentProcessor:

    def __init__(self, pdf_path: Path = PDF_PATH):
        self.pdf_path = Path(pdf_path)

        if not self.pdf_path.exists():
            raise FileNotFoundError(
                f"PDF not found: {self.pdf_path}"
            )

    def convert_pdf(self) -> str:
        print("\n[Document] Starting Docling...")

        converter = DocumentConverter()

        result = converter.convert(
            str(self.pdf_path)
        )

        markdown = result.document.export_to_markdown()

        print("[Document] PDF processed successfully.")
        print(
            f"[Document] Characters extracted: "
            f"{len(markdown)}"
        )

        return markdown

    def create_document(
        self,
        markdown: str,
    ) -> Document:

        document = Document(
            text=markdown,
            metadata={
                "source": self.pdf_path.name,
                "file_path": str(self.pdf_path),
                "document_type": "PDF",
                "title": "Bhagavad Gita",
            },
        )

        return document

    def create_chunks(
        self,
        document: Document,
    ) -> List:
        
        print("\n[Document] Creating chunks...")

        splitter = SentenceSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )

        nodes = splitter.get_nodes_from_documents(
            [document]
        )

        # Add chunk-level metadata
        for index, node in enumerate(nodes):

            node.metadata["chunk_id"] = index

            node.metadata["source"] = (
                self.pdf_path.name
            )

            node.metadata["document_type"] = "PDF"

            node.metadata["title"] = "Bhagavad Gita"

        print(
            f"[Document] Total chunks: {len(nodes)}"
        )

        return nodes

    def process(self) -> List:
        

        markdown = self.convert_pdf()

        document = self.create_document(
            markdown
        )

        nodes = self.create_chunks(
            document
        )

        return nodes


def main():

    print("=" * 60)
    print("DOCUMENT PROCESSOR TEST")
    print("=" * 60)

    processor = DocumentProcessor()

    nodes = processor.process()

    print("\n" + "=" * 60)
    print("TEST RESULT")
    print("=" * 60)

    print(f"Chunks created: {len(nodes)}")

    if nodes:

        print("\nFirst chunk preview:")
        print("-" * 60)

        print(
            nodes[0].get_content()[:1000]
        )

        print("-" * 60)

        print("\nFirst chunk metadata:")

        for key, value in nodes[0].metadata.items():
            print(f"{key}: {value}")

    print("=" * 60)


if __name__ == "__main__":
    main()