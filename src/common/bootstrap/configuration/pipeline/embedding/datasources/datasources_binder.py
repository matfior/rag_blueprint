from typing import Type

from atlassian import Confluence
from injector import singleton
from notion_client import Client

from common.bootstrap.base_binder import BaseBinder
from common.bootstrap.configuration.pipeline.embedding.datasources.datasources_binding_keys import (
    BoundDatasourceManagers,
)
from common.bootstrap.configuration.pipeline.embedding.datasources.datasources_configuration import (
    ConfluenceDatasourceConfiguration,
    DatasourceName,
    HackerNewsDatasourceConfiguration,
    NotionDatasourceConfiguration,
    PdfDatasourceConfiguration,
)
from embedding.datasources.confluence.builders import (
    ConfluenceCleanerBuilder,
    ConfluenceClientBuilder,
    ConfluenceDatasourceManagerBuilder,
    ConfluenceReaderBuilder,
    ConfluenceSplitterBuilder,
)
from embedding.datasources.confluence.cleaner import ConfluenceCleaner
from embedding.datasources.confluence.manager import ConfluenceDatasourceManager
from embedding.datasources.confluence.reader import ConfluenceReader
from embedding.datasources.confluence.splitter import ConfluenceSplitter
from embedding.datasources.hackernews.builders import (
    HackerNewsCleanerBuilder,
    HackerNewsDatasourceManagerBuilder,
    HackerNewsReaderBuilder,
    HackerNewsSplitterBuilder,
)
from embedding.datasources.hackernews.cleaner import HackerNewsCleaner
from embedding.datasources.hackernews.manager import HackerNewsDatasourceManager
from embedding.datasources.hackernews.reader import HackerNewsReader
from embedding.datasources.hackernews.splitter import HackerNewsSplitter
from embedding.datasources.notion.builders import (
    NotionCleanerBuilder,
    NotionClientBuilder,
    NotionDatasourceManagerBuilder,
    NotionExporterBuilder,
    NotionReaderBuilder,
    NotionSplitterBuilder,
)
from embedding.datasources.notion.cleaner import NotionCleaner
from embedding.datasources.notion.exporter import NotionExporter
from embedding.datasources.notion.manager import NotionDatasourceManager
from embedding.datasources.notion.reader import NotionReader
from embedding.datasources.notion.splitter import NotionSplitter
from embedding.datasources.pdf.builders import (
    PdfDatasourceManagerBuilder,
    PdfReaderBuilder,
)
from embedding.datasources.pdf.manager import PdfDatasourceManager
from embedding.datasources.pdf.reader import PdfReader
from embedding.embedders.builders import EmbedderBuilder
from embedding.embedders.default_embedder import Embedder
from embedding.orchestrators.builders import DatasourceOrchestratorBuilder
from embedding.orchestrators.datasource_orchestrator import (
    DatasourceOrchestrator,
)
from embedding.validators.builders import DatasourceValidatorBuilder
from embedding.validators.datasource_validator import DatasourceValidator


class NotionDatasourceBinder(BaseBinder):
    """Binder for the Notion datasources components."""

    def bind(self) -> Type:
        """Bind the Notion datasources components.

        Returns:
            Type: The Notion datasource manager."""
        self._bind_notion_cofuguration()
        self._bind_exporter()
        self._bind_client()
        self._bind_reader()
        self._bind_cleaner()
        self._bind_splitter()
        self._bind_manager()
        return NotionDatasourceManager

    def _bind_notion_cofuguration(self) -> None:
        """Bind the Notion datasource configuration."""
        notion_configuration = [
            configuration
            for configuration in self.configuration.pipeline.embedding.datasources
            if isinstance(configuration, NotionDatasourceConfiguration)
        ][0]
        self.binder.bind(
            NotionDatasourceConfiguration,
            to=notion_configuration,
            scope=singleton,
        )

    def _bind_exporter(self) -> None:
        """Bind the Notion exporter."""
        self.binder.bind(
            NotionExporter,
            to=NotionExporterBuilder.build,
        )

    def _bind_client(self) -> None:
        """Bind the Notion client."""
        self.binder.bind(
            Client,
            to=NotionClientBuilder.build,
        )

    def _bind_reader(self) -> None:
        """Bind the Notion reader."""
        self.binder.bind(
            NotionReader,
            to=NotionReaderBuilder.build,
        )

    def _bind_cleaner(self) -> None:
        """Bind the Notion cleaner."""
        self.binder.bind(
            NotionCleaner,
            to=NotionCleanerBuilder.build,
        )

    def _bind_splitter(self) -> None:
        """Bind the Notion splitter."""
        self.binder.bind(
            NotionSplitter,
            to=NotionSplitterBuilder.build,
        )

    def _bind_manager(self) -> None:
        """Bind the Notion datasource manager."""
        self.binder.bind(
            NotionDatasourceManager,
            to=NotionDatasourceManagerBuilder.build,
        )


class ConfluenceBinder(BaseBinder):
    """Binder for the Confluence datasources components."""

    def bind(self) -> Type:
        """Bind the Confluence datasources components.

        Returns:
            Type: The Confluence datasource manager."""
        self._bind_confluence_cofuguration()
        self._bind_client()
        self._bind_reader()
        self._bind_cleaner()
        self._bind_splitter()
        self._bind_manager()
        return ConfluenceDatasourceManager

    def _bind_confluence_cofuguration(self) -> None:
        """Bind the Confluence datasource configuration."""
        confluence_configuration = [
            configuration
            for configuration in self.configuration.pipeline.embedding.datasources
            if isinstance(configuration, ConfluenceDatasourceConfiguration)
        ][0]
        self.binder.bind(
            ConfluenceDatasourceConfiguration,
            to=confluence_configuration,
            scope=singleton,
        )

    def _bind_client(self) -> None:
        """Bind the Confluence client."""
        self.binder.bind(
            Confluence,
            to=ConfluenceClientBuilder.build,
        )

    def _bind_reader(self) -> None:
        """Bind the Confluence reader."""
        self.binder.bind(
            ConfluenceReader,
            to=ConfluenceReaderBuilder.build,
        )

    def _bind_cleaner(self) -> None:
        """Bind the Confluence cleaner."""
        self.binder.bind(ConfluenceCleaner, to=ConfluenceCleanerBuilder.build)

    def _bind_splitter(self) -> None:
        """Bind the Confluence splitter."""
        self.binder.bind(
            ConfluenceSplitter,
            to=ConfluenceSplitterBuilder.build,
        )

    def _bind_manager(self) -> None:
        """Bind the Confluence datasource manager."""
        self.binder.bind(
            ConfluenceDatasourceManager,
            to=ConfluenceDatasourceManagerBuilder.build,
        )


class PdfDatasourcesBinder(BaseBinder):
    """Binder for the PDF datasources components."""

    def bind(self) -> Type:
        """Bind the PDF datasources components.

        Returns:
            Type: The PDF datasource manager."""
        self._bind_pdf_configuration()
        self._bind_reader()
        self._bind_manager()
        return PdfDatasourceManager

    def _bind_pdf_configuration(self) -> None:
        """Bind the PDF datasource configuration."""
        confluence_configuration = [
            configuration
            for configuration in self.configuration.pipeline.embedding.datasources
            if isinstance(configuration, PdfDatasourceConfiguration)
        ][0]
        self.binder.bind(
            PdfDatasourceConfiguration,
            to=confluence_configuration,
            scope=singleton,
        )

    def _bind_reader(self) -> None:
        """Bind the PDF reader."""
        self.binder.bind(
            PdfReader,
            to=PdfReaderBuilder.build,
        )

    def _bind_manager(self) -> None:
        """Bind the PDF datasource manager."""
        self.binder.bind(
            PdfDatasourceManager,
            to=PdfDatasourceManagerBuilder.build,
        )


class DatasourcesBinder(BaseBinder):
    """Binder for the datasources components.

    Bind the list of datasource managers based on the configuration."""

    mapping = {
        DatasourceName.CONFLUENCE: ConfluenceBinder,
        DatasourceName.NOTION: NotionDatasourceBinder,
        DatasourceName.PDF: PdfDatasourcesBinder,
    }

    def bind(self) -> None:
        self._bind_datasource_managers()
        self._bind_embedder()
        self._bind_datasource_orchestrator()

    def _bind_datasource_managers(self) -> None:
        """Bind the datasource managers.

        Bind the datasource managers based on the configuration."""
        datasources_configuration = (
            self.configuration.pipeline.embedding.datasources
        )
        datasources = {}

        for datasource_configuration in datasources_configuration:
            datasource_manager_key = DatasourcesBinder.mapping[
                datasource_configuration.name
            ](configuration=self.configuration, binder=self.binder).bind()
            datasources[datasource_configuration.name] = self._get_bind(
                datasource_manager_key
            )()

        self.binder.bind(
            BoundDatasourceManagers,
            to=lambda: datasources,
            scope=singleton,
        )

    def _bind_embedder(self) -> None:
        """Bind the embedder."""
        self.binder.bind(
            Embedder,
            to=EmbedderBuilder.build,
        )

    def _bind_datasource_orchestrator(self) -> None:
        """Bind the datasource orchestrator."""
        self.binder.bind(
            DatasourceOrchestrator,
            to=DatasourceOrchestratorBuilder.build,
            scope=singleton,
        )

    def configure_hackernews_datasource(self, binder):
        """Configure HackerNews datasource bindings.

        Args:
            binder: Injector binder for dependency registration
        """
        # Bind HackerNews configuration
        binder.bind(
            HackerNewsDatasourceConfiguration,
            to=self._get_datasource_configuration(DatasourceName.HACKERNEWS),
            scope=singleton,
        )

        # Bind HackerNews reader
        binder.bind(
            HackerNewsReader,
            to=HackerNewsReaderBuilder.build,
            scope=singleton,
        )

        # Bind HackerNews cleaner
        binder.bind(
            HackerNewsCleaner,
            to=HackerNewsCleanerBuilder.build,
            scope=singleton,
        )

        # Bind HackerNews splitter
        binder.bind(
            HackerNewsSplitter,
            to=HackerNewsSplitterBuilder.build,
            scope=singleton,
        )

        # Bind HackerNews datasource manager
        binder.bind(
            HackerNewsDatasourceManager,
            to=HackerNewsDatasourceManagerBuilder.build,
            scope=singleton,
        )

    def configure(self, binder):
        """Configure all datasource bindings.

        Args:
            binder: Injector binder for dependency registration
        """
        # Bind datasource managers
        datasource_managers = []

        # Configure datasources based on configuration
        for datasource_config in self.configuration.datasources:
            if datasource_config.name == DatasourceName.NOTION:
                self.configure_notion_datasource(binder)
                datasource_managers.append(NotionDatasourceManager)
            elif datasource_config.name == DatasourceName.CONFLUENCE:
                self.configure_confluence_datasource(binder)
                datasource_managers.append(ConfluenceDatasourceManager)
            elif datasource_config.name == DatasourceName.PDF:
                self.configure_pdf_datasource(binder)
                datasource_managers.append(PdfDatasourceManager)
            elif datasource_config.name == DatasourceName.HACKERNEWS:
                self.configure_hackernews_datasource(binder)
                datasource_managers.append(HackerNewsDatasourceManager)

        # Bind datasource managers list
        binder.bind(
            BoundDatasourceManagers,
            to=datasource_managers,
            scope=singleton,
        )

        # Bind datasource validator
        binder.bind(
            DatasourceValidator,
            to=DatasourceValidatorBuilder.build,
            scope=singleton,
        )

        # Bind datasource orchestrator
        binder.bind(
            DatasourceOrchestrator,
            to=DatasourceOrchestratorBuilder.build,
            scope=singleton,
        )

        # Bind embedder
        binder.bind(
            Embedder,
            to=EmbedderBuilder.build,
            scope=singleton,
        )
