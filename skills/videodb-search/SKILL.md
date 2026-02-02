---
name: videodb-search
description: Search within videos and video collections using natural language queries. Use this skill when users want to find specific moments, topics, or content in their VideoDB videos. Supports semantic search (meaning-based) and keyword search (exact match). Triggers on "find in video", "search for", "where do they mention", "locate in videos".
---

# VideoDB Search

Search your video library using natural language to find specific moments without watching entire videos.

## Setup

1. **Install dependencies** (one-time):
```bash
cd skills/videodb-search
./setup.sh
```

2. **Configure API key** - Add to `skills/.env`:
```
VIDEODB_API_KEY=your-api-key
```

## Quick Start

```python
from videodb import connect, SearchType, IndexType

conn = connect()
video = conn.get_collection().get_video("video_id")

# Index first (one-time)
video.index_spoken_words()

# Search
results = video.search(query="pricing discussion", search_type=SearchType.semantic)
stream_url = results.compile()
```

## When to Use

- User wants to "find", "search", or "locate" content in videos
- User asks "where do they talk about X"
- User needs clips matching specific criteria

## Search Types

### Semantic (Default)
Searches by meaning - best for questions and topics.
```python
results = video.search(query="What do they say about pricing?", search_type=SearchType.semantic)
```

### Keyword
Exact phrase matching - best for specific terms.
```python
results = video.search(query="quarterly report", search_type=SearchType.keyword)
```
**Note:** Keyword search only works on single videos, not collections.

## Prerequisites

**Important:** Videos must be indexed before searching. Without indexing, searches will fail with `NOT_INDEXED` error.

```python
# Index spoken content (required for spoken_word search)
video.index_spoken_words()

# Index visual content (required for scene search)
video.index_scenes(prompt="Describe what you see")
```

Indexing is a one-time operation per video. It may take 1-5 minutes depending on video length.

## Working with Results

```python
results = video.search(query="your query")

# Get individual clips
for shot in results.get_shots():
    print(f"{shot.start}s - {shot.end}s: {shot.text}")
    print(f"Score: {shot.score}, URL: {shot.stream_url}")

# Get combined stream of all results
compiled_url = results.compile()
```

## Collection Search

Search across all videos:
```python
collection = conn.get_collection()
results = collection.search(query="customer feedback")
```

## Scripts

Use the unified `run.sh` from the skills directory:
```bash
# From the skills/ directory:
./run.sh search '{"url": "https://youtu.be/xxx", "query": "topic"}'

# Search by video ID
./run.sh search '{"video_id": "vid_123", "query": "pricing"}'

# Search entire collection
./run.sh search '{"query": "product demo", "scope": "collection"}'
```

Or run directly with Python (requires venv activated):
```bash
cd skills/
source venv/bin/activate
python videodb-search/scripts/search.py '{"url": "https://youtu.be/xxx", "query": "topic"}'
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | str | required | Search query |
| `url` | str | optional | YouTube URL (auto-uploads video) |
| `video_id` | str | optional | VideoDB video ID |
| `search_type` | str | semantic | `semantic` or `keyword` |
| `index_type` | str | spoken_word | `spoken_word` or `scene` |
| `result_threshold` | int | 5 | Max results |
| `score_threshold` | float | 0.2 | Min relevance (0-1) |

## Common Errors

| Error | Solution |
|-------|----------|
| MISSING_DEPENDENCY | Run `./setup.sh` to install videodb |
| MISSING_API_KEY | Add VIDEODB_API_KEY to `skills/.env` |
| NOT_INDEXED | Auto-handled - script indexes automatically |
| VIDEO_NOT_FOUND | Check video ID exists |
| NO_RESULTS | Broaden query or lower score_threshold |