from injector import inject

from common.bootstrap.configuration.pipeline.embedding.datasources.datasources_configuration import (
    HackerNewsDatasourceConfiguration,
)
from common.bootstrap.configuration.pipeline.embedding.embedding_model.embedding_model_binding_keys import (
    BoundEmbeddingModelMarkdownSplitter,
)
from embedding.datasources.hackernews.cleaner import HackerNewsCleaner
from embedding.datasources.hackernews.manager import HackerNewsDatasourceManager
from embedding.datasources.hackernews.reader import HackerNewsReader
from embedding.datasources.hackernews.splitter import HackerNewsSplitter


class HackerNewsReaderBuilder:
    """Builder for creating HackerNews reader instances.

    Provides factory method to create configured HackerNewsReader
    with required settings.
    """

    @staticmethod
    @inject
    def build(
        configuration: HackerNewsDatasourceConfiguration,
    ) -> HackerNewsReader:
        """Creates a configured HackerNews reader.

        Args:
            configuration: HackerNews access and processing settings

        Returns:
            HackerNewsReader: Configured reader instance
        """
        return HackerNewsReader(
            export_limit=configuration.export_limit,
            export_batch_size=configuration.export_batch_size,
            base_url=configuration.base_url,
        )


class HackerNewsCleanerBuilder:
    """Builder for creating HackerNews cleaner instances.

    Provides factory method to create HackerNewsCleaner instances.
    """

    @staticmethod
    def build() -> HackerNewsCleaner:
        """Creates a HackerNews cleaner.

        Returns:
            HackerNewsCleaner: Cleaner instance
        """
        return HackerNewsCleaner()


class HackerNewsSplitterBuilder:
    """Builder for creating HackerNews splitter instances.

    Provides factory method to create configured HackerNewsSplitter
    with required components.
    """

    @staticmethod
    @inject
    def build(
        markdown_parser: BoundEmbeddingModelMarkdownSplitter,
    ) -> HackerNewsSplitter:
        """Creates a configured HackerNews splitter.

        Args:
            markdown_parser: Parser for markdown content

        Returns:
            HackerNewsSplitter: Configured splitter instance
        """
        return HackerNewsSplitter(markdown_parser=markdown_parser)


class HackerNewsDatasourceManagerBuilder:
    """Builder for creating HackerNews datasource manager instances.

    Provides factory method to create configured HackerNewsDatasourceManager
    with required components for content processing.
    """

    @staticmethod
    @inject
    def build(
        reader: HackerNewsReader,
        cleaner: HackerNewsCleaner,
        splitter: HackerNewsSplitter,
    ) -> HackerNewsDatasourceManager:
        """Creates a configured HackerNews datasource manager.

        Args:
            reader: Component for reading HackerNews content
            cleaner: Component for cleaning raw content
            splitter: Component for splitting content into chunks

        Returns:
            HackerNewsDatasourceManager: Configured manager instance
        """
        return HackerNewsDatasourceManager(
            reader=reader,
            cleaner=cleaner,
            splitter=splitter,
        ) 