# HackerNews Data Source

This module implements a data source for the HackerNews API, allowing the RAG blueprint to fetch and process stories from HackerNews.

## Overview

The HackerNews API provides access to stories, comments, and other content from HackerNews. This implementation focuses on retrieving top stories and processing them for use in the RAG pipeline.

## Features

- Fetches top stories from the HackerNews API
- Processes story content and metadata
- Supports configurable batch sizes and export limits
- Implements asynchronous fetching for improved performance

## Configuration

To use the HackerNews data source, add the following configuration to your `configuration.json` file:

```json
{
    "name": "hackernews",
    "export_limit": 20,
    "export_batch_size": 5,
    "base_url": "https://hacker-news.firebaseio.com/v0"
}
```

### Configuration Options

- `name`: Must be set to "hackernews"
- `export_limit`: Maximum number of stories to fetch (optional)
- `export_batch_size`: Number of stories to fetch concurrently (default: 10)
- `base_url`: Base URL for the HackerNews API (default: "https://hacker-news.firebaseio.com/v0")

## Implementation Details

The HackerNews data source implementation consists of the following components:

- `HackerNewsDocument`: Represents a story from HackerNews
- `HackerNewsReader`: Fetches stories from the HackerNews API
- `HackerNewsCleaner`: Cleans the content of HackerNews stories
- `HackerNewsSplitter`: Splits HackerNews stories into chunks for embedding
- `HackerNewsDatasourceManager`: Coordinates the extraction, cleaning, and splitting of HackerNews content

## API Endpoints Used

- `/topstories.json`: Retrieves IDs of top stories
- `/item/{id}.json`: Retrieves details of a specific story

## Example Usage

Once configured, the HackerNews data source will be automatically used by the RAG pipeline. No additional code is required to use it.

## Limitations

- Only fetches top stories, not new or best stories
- Does not fetch comments or other content types
- Rate limiting is not implemented, but the API is generally not rate-limited 