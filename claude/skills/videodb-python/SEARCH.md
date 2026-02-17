# Search & Indexing Guide

Search allows you to find specific moments inside videos using natural language queries, exact keywords, or visual scene descriptions.

## Prerequisites

Videos **must be indexed** before they can be searched. Indexing is a one-time operation per video per index type.

## Indexing

### Spoken Word Index

Index the transcribed speech content of a video for semantic and keyword search:

```python
video = coll.get_video(video_id)
video.index_spoken_words()
```

This transcribes the audio track and builds a searchable index over the spoken content. Required for semantic search and keyword search.

### Scene Index

Index visual content by generating AI descriptions of scenes:

```python
from videodb import SceneExtractionType

# Extract scenes and index them
video.index_scenes(
    extraction_type=SceneExtractionType.shot_based,
    prompt="Describe the visual content, objects, actions, and setting in this scene.",
)
```

**Extraction types:**

| Type | Description | Best For |
|------|-------------|----------|
| `SceneExtractionType.shot_based` | Splits on visual shot boundaries | General purpose, action content |
| `SceneExtractionType.time_based` | Splits at fixed intervals | Uniform sampling, long static content |

**Parameters for `time_based`:**

```python
video.index_scenes(
    extraction_type=SceneExtractionType.time_based,
    extraction_config={"time": 5, "select_frames": ["first", "last"]},
    prompt="Describe what is happening in this scene.",
)
```

## Search Types

### Semantic Search

Natural language queries matched against spoken content:

```python
from videodb import SearchType

results = video.search(
    query="explaining the benefits of machine learning",
    search_type=SearchType.semantic,
)
```

Returns ranked segments where the spoken content semantically matches the query.

### Keyword Search

Exact term matching in transcribed speech:

```python
results = video.search(
    query="artificial intelligence",
    search_type=SearchType.keyword,
)
```

Returns segments containing the exact keyword or phrase.

### Scene Search

Visual content queries matched against indexed scene descriptions:

```python
from videodb import SearchType, IndexType

results = video.search(
    query="person writing on a whiteboard",
    search_type=SearchType.scene,
    index_type=IndexType.scene,
)
```

Requires prior `index_scenes()` call. Returns segments where the visual content matches the query.

> **Note:** `SearchType.scene` may not be available on all plans (e.g. Free tier). If you get an error, use `SearchType.semantic` with `index_type=IndexType.scene` as an alternative:

```python
results = video.search(
    query="person writing on a whiteboard",
    search_type=SearchType.semantic,
    index_type=IndexType.scene,
)
```

## Working with Results

### Get Shots

Access individual result segments:

```python
results = video.search("your query")

for shot in results.get_shots():
    print(f"Video: {shot.video_id}")
    print(f"Start: {shot.start:.2f}s")
    print(f"End: {shot.end:.2f}s")
    print(f"Text: {shot.text}")
    print("---")
```

### Play Compiled Results

Stream all matching segments as a single compiled video:

```python
results = video.search("your query")
stream_url = results.compile()
results.play()  # opens compiled stream in browser
```

### Extract Clips

Download or stream specific result segments:

```python
from videodb import play_stream

for shot in results.get_shots():
    stream_url = shot.generate_stream()
    print(f"Clip: {stream_url}")
```

## Cross-Collection Search

Search across all videos in a collection:

```python
coll = conn.get_collection()

# Search across all videos in the collection
results = coll.search(
    query="product demo",
    search_type=SearchType.semantic,
)

for shot in results.get_shots():
    print(f"Video: {shot.video_id} [{shot.start:.1f}s - {shot.end:.1f}s]")
```

## Search + Compilation Workflow

For a complete automated workflow, use the helper script:

```bash
python scripts/search_and_compile.py --video-id <id> --query "your query"
```

This indexes (if needed), searches, compiles results, and returns a stream URL.

## Tips

- **Index once, search many times**: Indexing is the expensive operation. Once indexed, searches are fast.
- **Combine index types**: Index both spoken words and scenes to enable all search types on the same video.
- **Refine queries**: Semantic search works best with descriptive, natural language phrases rather than single keywords.
- **Use keyword search for precision**: When you need exact term matches, keyword search avoids semantic drift.
