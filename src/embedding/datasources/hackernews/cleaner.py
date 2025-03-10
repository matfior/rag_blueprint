import logging
import re
from typing import List

from embedding.datasources.core.cleaner import BaseCleaner
from embedding.datasources.hackernews.document import HackerNewsDocument


class HackerNewsCleaner(BaseCleaner):
    """Cleaner for HackerNews content.

    Implements cleaning operations specific to HackerNews stories,
    including HTML tag removal and content normalization.

    Attributes:
        logger: Logger instance for tracking cleaning operations
    """

    def __init__(self):
        """Initialize HackerNews cleaner."""
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def clean_documents(self, documents: List[HackerNewsDocument]) -> List[HackerNewsDocument]:
        """Clean a list of HackerNews documents.

        Args:
            documents: List of documents to clean

        Returns:
            List[HackerNewsDocument]: Cleaned documents
        """
        self.logger.info(f"Cleaning {len(documents)} HackerNews documents")
        
        cleaned_documents = []
        for document in documents:
            try:
                cleaned_document = self.clean_document(document)
                cleaned_documents.append(cleaned_document)
            except Exception as e:
                self.logger.error(f"Error cleaning document: {e}")
        
        self.logger.info(f"Cleaned {len(cleaned_documents)} HackerNews documents")
        return cleaned_documents

    def clean_document(self, document: HackerNewsDocument) -> HackerNewsDocument:
        """Clean a single HackerNews document.

        Args:
            document: Document to clean

        Returns:
            HackerNewsDocument: Cleaned document
        """
        # Clean the text content
        cleaned_text = self._clean_text(document.text)
        
        # Create a new document with cleaned text
        cleaned_document = HackerNewsDocument(
            text=cleaned_text,
            metadata=document.metadata,
            attachments=document.attachments,
        )
        
        # Copy metadata filtering settings
        cleaned_document.excluded_embed_metadata_keys = document.excluded_embed_metadata_keys
        cleaned_document.excluded_llm_metadata_keys = document.excluded_llm_metadata_keys
        
        return cleaned_document

    def _clean_text(self, text: str) -> str:
        """Clean text content from HackerNews.

        Args:
            text: Raw text content

        Returns:
            str: Cleaned text
        """
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Convert HTML entities
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        text = text.replace('&#x27;', "'")
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Normalize line breaks
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        return text.strip() 