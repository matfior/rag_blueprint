import logging
from typing import List

from llama_index.core.node_parser import MarkdownNodeParser

from embedding.datasources.core.splitter import BaseSplitter
from embedding.datasources.hackernews.document import HackerNewsDocument


class HackerNewsSplitter(BaseSplitter):
    """Splitter for HackerNews content.

    Implements content splitting for HackerNews stories using
    markdown-aware node parsing.

    Attributes:
        markdown_parser: Parser for markdown content
        logger: Logger instance for tracking splitting operations
    """

    def __init__(self, markdown_parser: MarkdownNodeParser):
        """Initialize HackerNews splitter.

        Args:
            markdown_parser: Parser for markdown content
        """
        super().__init__()
        self.markdown_parser = markdown_parser
        self.logger = logging.getLogger(__name__)

    def split_documents(self, documents: List[HackerNewsDocument]) -> List[HackerNewsDocument]:
        """Split a list of HackerNews documents.

        Args:
            documents: List of documents to split

        Returns:
            List[HackerNewsDocument]: Split documents
        """
        self.logger.info(f"Splitting {len(documents)} HackerNews documents")
        
        split_documents = []
        for document in documents:
            try:
                # Parse the document into nodes
                nodes = self.markdown_parser.get_nodes_from_documents([document])
                
                # Create a new document for each node
                for node in nodes:
                    # Create a new document with the node text
                    split_document = HackerNewsDocument(
                        text=node.text,
                        metadata=document.metadata,
                        attachments=document.attachments,
                    )
                    
                    # Copy metadata filtering settings
                    split_document.excluded_embed_metadata_keys = document.excluded_embed_metadata_keys
                    split_document.excluded_llm_metadata_keys = document.excluded_llm_metadata_keys
                    
                    split_documents.append(split_document)
            except Exception as e:
                self.logger.error(f"Error splitting document: {e}")
                # If splitting fails, keep the original document
                split_documents.append(document)
        
        self.logger.info(f"Split into {len(split_documents)} HackerNews documents")
        return split_documents 