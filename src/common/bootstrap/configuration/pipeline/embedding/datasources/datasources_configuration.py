from abc import ABC
from enum import Enum
from typing import Literal, Optional, Union

from pydantic import ConfigDict, Field, SecretStr
from pydantic_settings import BaseSettings

from common.bootstrap.secrets_configuration import ConfigurationWithSecrets

# Enums


class DatasourceName(str, Enum):
    NOTION = "notion"
    CONFLUENCE = "confluence"
    PDF = "pdf"
    HACKERNEWS = "hackernews"


# Secrets


class NotionSecrets(BaseSettings):
    model_config = ConfigDict(
        env_file_encoding="utf-8",
        env_prefix="RAG__DATASOURCES__NOTION__",
        env_nested_delimiter="__",
        extra="ignore",
    )

    api_token: SecretStr = Field(
        ..., description="The token for the notion data source"
    )


class ConfluenceSecrets(BaseSettings):
    model_config = ConfigDict(
        env_file_encoding="utf-8",
        env_prefix="RAG__DATASOURCES__CONFLUENCE__",
        env_nested_delimiter="__",
        extra="ignore",
    )

    username: SecretStr = Field(
        ...,
        description="The username for the confluence data source",
    )
    password: SecretStr = Field(
        ...,
        description="The password for the confluence data source",
    )


class PdfSecrets(BaseSettings):
    model_config = ConfigDict(
        extra="ignore",
    )


class HackerNewsSecrets(BaseSettings):
    model_config = ConfigDict(
        extra="ignore",
    )


# Configuration


class DatasourceConfiguration(ConfigurationWithSecrets, ABC):
    name: DatasourceName = Field(
        ..., description="The name of the data source."
    )
    export_limit: Optional[int] = Field(
        None, description="The export limit for the data source."
    )


class ConfluenceDatasourceConfiguration(DatasourceConfiguration):
    host: str = Field(
        "127.0.0.1", description="Host of the vector store server"
    )
    protocol: Union[Literal["http"], Literal["https"]] = Field(
        "http", description="The protocol for the vector store."
    )
    name: Literal[DatasourceName.CONFLUENCE] = Field(
        ..., description="The name of the data source."
    )
    secrets: ConfluenceSecrets = Field(
        None, description="The secrets for the data source."
    )

    @property
    def base_url(self) -> str:
        return f"{self.protocol}://{self.host}"


class NotionDatasourceConfiguration(DatasourceConfiguration):
    name: Literal[DatasourceName.NOTION] = Field(
        ..., description="The name of the data source."
    )
    home_page_database_id: Optional[str] = Field(
        None,
        description="Notion home page database id used for extraction of pages and database. If null, this extraction will be skipped.",
    )
    export_batch_size: int = Field(
        3,
        description="Number of pages being exported ansychronously. Decrease to avoid NotionAPI rate limits, smaller batch slows the export down.",
    )
    secrets: NotionSecrets = Field(
        None, description="The secrets for the data source."
    )


class PdfDatasourceConfiguration(DatasourceConfiguration):
    name: Literal[DatasourceName.PDF] = Field(
        ..., description="The name of the data source."
    )
    base_path: str = Field(
        ..., description="Base path to the directory containing PDF files"
    )
    nlm_parser_enabled: bool = Field(
        False, description="Use NLM parser for PDF files"
    )
    nlm_parser_api_base: str = Field(
        None, description="NLM parser API base URL"
    )
    secrets: PdfSecrets = Field(
        None, description="The secrets for the data source."
    )


class HackerNewsDatasourceConfiguration(DatasourceConfiguration):
    name: Literal[DatasourceName.HACKERNEWS] = Field(
        ..., description="The name of the data source."
    )
    export_batch_size: int = Field(
        10,
        description="Number of stories being exported asynchronously. Adjust to balance speed and API load.",
    )
    base_url: str = Field(
        "https://hacker-news.firebaseio.com/v0",
        description="Base URL for the HackerNews API",
    )
    secrets: HackerNewsSecrets = Field(
        None, description="The secrets for the data source."
    )


AVAIALBLE_DATASOURCES = Union[
    NotionDatasourceConfiguration,
    ConfluenceDatasourceConfiguration,
    PdfDatasourceConfiguration,
    HackerNewsDatasourceConfiguration,
]
