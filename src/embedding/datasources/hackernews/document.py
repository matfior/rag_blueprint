from embedding.datasources.core.document import BaseDocument


class HackerNewsDocument(BaseDocument):
    """Document representation for HackerNews story content.

    Extends BaseDocument to handle HackerNews-specific document processing including
    metadata handling and filtering for embeddings and LLM contexts.

    Attributes:
        attachments: Dictionary of document attachments
        text: Document content in markdown format
        metadata: Extracted story metadata including dates and source info
        excluded_embed_metadata_keys: Metadata keys to exclude from embeddings
        excluded_llm_metadata_keys: Metadata keys to exclude from LLM context
    """

    @classmethod
    def from_story(cls, metadata: dict, text: str) -> "HackerNewsDocument":
        """Create HackerNewsDocument instance from story data.

        Args:
            metadata: Dictionary containing story metadata
            text: Extracted story content

        Returns:
            HackerNewsDocument: Configured document instance
        """
        document = cls(
            attachments={},
            text=text,
            metadata=HackerNewsDocument._get_metadata(metadata),
        )
        document._set_excluded_embed_metadata_keys()
        document._set_excluded_llm_metadata_keys()
        return document

    def _set_excluded_embed_metadata_keys(self) -> None:
        """Configure metadata keys to exclude from embeddings.

        Identifies metadata keys not explicitly included in embedding
        processing and marks them for exclusion.
        """
        metadata_keys = self.metadata.keys()
        self.excluded_embed_metadata_keys = [
            key
            for key in metadata_keys
            if key not in self.included_embed_metadata_keys
        ]

    def _set_excluded_llm_metadata_keys(self) -> None:
        """Configure metadata keys to exclude from LLM context.

        Identifies metadata keys not explicitly included in LLM
        processing and marks them for exclusion.
        """
        metadata_keys = self.metadata.keys()
        self.excluded_llm_metadata_keys = [
            key
            for key in metadata_keys
            if key not in self.included_llm_metadata_keys
        ]

    @staticmethod
    def _get_metadata(metadata: dict) -> dict:
        """Process and enhance story metadata.

        Args:
            metadata: Raw story metadata dictionary

        Returns:
            dict: Enhanced metadata including source and formatted dates
        """
        metadata["datasource"] = "hackernews"
        
        # Convert Unix timestamp to ISO format if available
        if "time" in metadata:
            from datetime import datetime
            timestamp = metadata.get("time", 0)
            dt = datetime.fromtimestamp(timestamp)
            iso_time = dt.isoformat()
            metadata["created_time"] = iso_time
            metadata["created_date"] = iso_time.split("T")[0]
            
        # Add URL to the story if available
        if "id" in metadata:
            metadata["url"] = f"https://news.ycombinator.com/item?id={metadata['id']}"
            
        return metadata 