"""Document processing utilities for RAG."""

from typing import List, Dict, Any
from pathlib import Path
import hashlib
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter


class DocumentProcessor:
    """Process documents for RAG ingestion."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """Initialize document processor.

        Args:
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )

    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text from PDF file.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text
        """
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks.

        Args:
            text: Text to split

        Returns:
            List of text chunks
        """
        return self.text_splitter.split_text(text)

    def process_document(
        self,
        file_path: Path,
        metadata: Dict[str, Any] | None = None
    ) -> tuple[List[str], List[Dict[str, Any]], List[str]]:
        """Process a document for ingestion.

        Args:
            file_path: Path to document
            metadata: Optional metadata for the document

        Returns:
            Tuple of (chunks, metadatas, ids)
        """
        # Extract text based on file type
        if file_path.suffix.lower() == ".pdf":
            text = self.extract_text_from_pdf(file_path)
        elif file_path.suffix.lower() == ".txt":
            text = file_path.read_text()
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")

        # Chunk the text
        chunks = self.chunk_text(text)

        # Create metadata for each chunk
        base_metadata = metadata or {}
        base_metadata["source"] = str(file_path.name)
        base_metadata["file_path"] = str(file_path)

        metadatas = [
            {**base_metadata, "chunk_index": i}
            for i in range(len(chunks))
        ]

        # Generate unique IDs for each chunk
        ids = [
            self._generate_chunk_id(file_path.name, i)
            for i in range(len(chunks))
        ]

        return chunks, metadatas, ids

    @staticmethod
    def _generate_chunk_id(filename: str, chunk_index: int) -> str:
        """Generate a unique ID for a document chunk.

        Args:
            filename: Name of the source file
            chunk_index: Index of the chunk

        Returns:
            Unique chunk ID
        """
        content = f"{filename}_{chunk_index}"
        return hashlib.md5(content.encode()).hexdigest()


# Global instance
document_processor = DocumentProcessor()
