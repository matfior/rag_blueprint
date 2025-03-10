import logging
import asyncio
import aiohttp
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

from embedding.datasources.core.reader import BaseReader
from embedding.datasources.hackernews.document import HackerNewsDocument


class HackerNewsReader(BaseReader):
    """Reader for extracting stories from HackerNews API.

    Implements document extraction from HackerNews stories with
    support for batched async operations and export limits.

    Attributes:
        export_limit: Maximum number of stories to export
        export_batch_size: Number of stories to fetch concurrently
        base_url: Base URL for the HackerNews API
    """

    def __init__(
        self,
        export_limit: Optional[int] = None,
        export_batch_size: int = 10,
        base_url: str = "https://hacker-news.firebaseio.com/v0",
    ):
        """Initialize HackerNews reader.

        Args:
            export_limit: Maximum number of stories to export (None for no limit)
            export_batch_size: Number of stories to fetch concurrently
            base_url: Base URL for the HackerNews API
        """
        super().__init__()
        self.export_limit = export_limit
        self.export_batch_size = export_batch_size
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)

    def get_all_documents(self) -> List[HackerNewsDocument]:
        """Synchronously retrieve all stories from HackerNews.

        Returns:
            List[HackerNewsDocument]: Collection of extracted documents
        """
        return asyncio.run(self.get_all_documents_async())

    async def get_all_documents_async(self) -> List[HackerNewsDocument]:
        """Asynchronously retrieve all stories from HackerNews.

        Returns:
            List[HackerNewsDocument]: Collection of extracted documents
        """
        self.logger.info("Starting HackerNews story extraction")
        
        # Get top story IDs
        story_ids = await self._get_top_story_ids()
        
        # Apply export limit if specified
        if self.export_limit is not None:
            story_ids = story_ids[:self.export_limit]
            self.logger.info(f"Limited to {self.export_limit} stories")
        
        # Fetch stories in batches
        documents = []
        for i in range(0, len(story_ids), self.export_batch_size):
            batch_ids = story_ids[i:i + self.export_batch_size]
            self.logger.info(f"Fetching batch of {len(batch_ids)} stories ({i+1}-{i+len(batch_ids)} of {len(story_ids)})")
            
            batch_docs = await self._fetch_stories_batch(batch_ids)
            documents.extend(batch_docs)
            
        self.logger.info(f"Extracted {len(documents)} HackerNews stories")
        return documents

    async def _get_top_story_ids(self) -> List[int]:
        """Fetch IDs of top stories from HackerNews API.

        Returns:
            List[int]: List of story IDs
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/topstories.json") as response:
                if response.status != 200:
                    self.logger.error(f"Failed to fetch top stories: {response.status}")
                    return []
                
                story_ids = await response.json()
                return story_ids

    async def _fetch_stories_batch(self, story_ids: List[int]) -> List[HackerNewsDocument]:
        """Fetch a batch of stories by their IDs.

        Args:
            story_ids: List of story IDs to fetch

        Returns:
            List[HackerNewsDocument]: List of documents created from stories
        """
        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch_story(session, story_id) for story_id in story_ids]
            stories = await asyncio.gather(*tasks)
            
            # Filter out None values (failed fetches)
            stories = [s for s in stories if s is not None]
            
            # Convert stories to documents
            documents = []
            for story in stories:
                try:
                    # Create text content from story
                    text = self._create_story_text(story)
                    
                    # Create document
                    document = HackerNewsDocument.from_story(story, text)
                    documents.append(document)
                except Exception as e:
                    self.logger.error(f"Error creating document for story {story.get('id')}: {e}")
            
            return documents

    async def _fetch_story(self, session: aiohttp.ClientSession, story_id: int) -> Optional[Dict[str, Any]]:
        """Fetch a single story by its ID.

        Args:
            session: HTTP session to use
            story_id: ID of the story to fetch

        Returns:
            Optional[Dict[str, Any]]: Story data or None if fetch failed
        """
        try:
            async with session.get(f"{self.base_url}/item/{story_id}.json") as response:
                if response.status != 200:
                    self.logger.error(f"Failed to fetch story {story_id}: {response.status}")
                    return None
                
                story = await response.json()
                return story
        except Exception as e:
            self.logger.error(f"Error fetching story {story_id}: {e}")
            return None

    def _create_story_text(self, story: Dict[str, Any]) -> str:
        """Create markdown text content from a story.

        Args:
            story: Story data

        Returns:
            str: Markdown formatted text
        """
        # Start with title as heading
        text = f"# {story.get('title', 'Untitled Story')}\n\n"
        
        # Add URL if available
        if "url" in story:
            text += f"URL: {story['url']}\n\n"
        
        # Add story text if available
        if "text" in story and story["text"]:
            text += f"{story['text']}\n\n"
        
        # Add metadata
        text += f"Points: {story.get('score', 0)}\n"
        text += f"Author: {story.get('by', 'unknown')}\n"
        
        # Add timestamp
        if "time" in story:
            dt = datetime.fromtimestamp(story["time"])
            text += f"Posted: {dt.strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        # Add comments count
        if "descendants" in story:
            text += f"Comments: {story['descendants']}\n"
        
        return text 