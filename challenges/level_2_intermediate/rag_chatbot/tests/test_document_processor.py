"""
Tests for document processor module.
Candidates should implement these tests.
"""

import pytest
from pathlib import Path
from challenges.level_2_intermediate.rag_chatbot.document_processor import (
    DocumentProcessor,
)


class TestDocumentProcessor:
    """Test cases for DocumentProcessor."""

    def test_processor_initialization(self) -> None:
        """Test that processor initializes correctly."""
        processor = DocumentProcessor()
        assert processor.chunk_size == 512
        assert processor.chunk_overlap == 50

    def test_load_documents_not_implemented(self) -> None:
        """Test that load_documents raises NotImplementedError."""
        processor = DocumentProcessor()
        with pytest.raises(NotImplementedError):
            processor.load_documents(Path("dummy_path"))

    # TODO: Add more test cases after implementation
