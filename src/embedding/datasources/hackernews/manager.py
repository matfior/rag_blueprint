from embedding.datasources.core.manager import BaseDatasourceManager
from embedding.datasources.hackernews.reader import HackerNewsReader
from embedding.datasources.hackernews.cleaner import HackerNewsCleaner
from embedding.datasources.hackernews.splitter import HackerNewsSplitter


class HackerNewsDatasourceManager(BaseDatasourceManager):
    """Manager for HackerNews data source.

    Coordinates extraction, cleaning, and splitting of HackerNews content.

    Attributes:
        reader: Component for extracting content
        cleaner: Component for cleaning content
        splitter: Component for splitting content
    """

    def __init__(
        self,
        reader: HackerNewsReader,
        cleaner: HackerNewsCleaner,
        splitter: HackerNewsSplitter,
    ):
        """Initialize HackerNews datasource manager.

        Args:
            reader: Component for extracting content
            cleaner: Component for cleaning content
            splitter: Component for splitting content
        """
        super().__init__(reader, cleaner, splitter) 