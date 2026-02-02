---
name: videodb-scene-index
description: Index and search visual content in videos. Use this skill when users want to find scenes based on visual elements like objects, people, actions, or settings. Supports custom prompts for specialized analysis like security footage, sports highlights, or product detection. Triggers on "find scenes", "visual search", "what's shown", "detect objects", "analyze footage".
---

# VideoDB Scene Index

Analyze and search video content based on visual elements - objects, people, actions, and scenes.

## Quick Start

```python
from videodb import connect, IndexType, SceneExtractionType

conn = connect()
video = conn.get_collection().get_video("video_id")

# Create scene index
video.index_scenes(
    extraction_type=SceneExtractionType.time_based,
    extraction_config={"time": 5, "frame_count": 3},
    prompt="Describe people, objects, and actions visible."
)

# Search visual content
results = video.search(query="person walking", index_type=IndexType.scene)
stream_url = results.compile()
```

## When to Use

- User wants to find "scenes" or "moments" based on visuals
- User asks "what's shown" or "what happens" in video
- User needs to detect objects, people, or actions
- User has security/surveillance footage to analyze
- User wants visual search (not based on speech)

## Scene Extraction Types

### Time-Based
Segments video at fixed intervals. Best for consistent content.
```python
video.index_scenes(
    extraction_type=SceneExtractionType.time_based,
    extraction_config={
        "time": 5,          # seconds per scene
        "frame_count": 3    # frames to analyze
    },
    prompt="Describe what you see."
)
```

### Shot-Based
Detects camera cuts automatically. Best for edited content.
```python
video.index_scenes(
    extraction_type=SceneExtractionType.shot_based,
    extraction_config={
        "threshold": 20,    # sensitivity (lower = more scenes)
        "frame_count": 3
    },
    prompt="Describe this scene."
)
```

## Custom Prompts

Prompts tell the vision model what to look for:

**General:**
```python
prompt = "Describe people, objects, setting, and actions visible."
```

**Security:**
```python
prompt = "Identify people, vehicles, and any unusual activity. Note 'ALERT' for concerns."
```

**Sports:**
```python
prompt = "Describe the play, player positions, and scoring actions."
```

**Products:**
```python
prompt = "Identify products, brands, and logos visible."
```

## Searching Scenes

After indexing, search with `index_type=IndexType.scene`:

```python
from videodb import IndexType

results = video.search(
    query="red car",
    index_type=IndexType.scene
)

for shot in results.get_shots():
    print(f"{shot.start}s - {shot.end}s: {shot.text}")
```

## Processing Time

| Video Length | Time |
|--------------|------|
| 5 min | 1-3 min |
| 15 min | 3-7 min |
| 30 min | 7-15 min |

**Note:** Scene indexing runs asynchronously. After calling `index_scenes()`, the index status will be `processing` until complete. You can check status with `video.list_scene_index()` and search once status is `ready`.

## Scripts

Run `scripts/scene_index.py` for programmatic access:
```bash
# Create index
python scripts/scene_index.py '{"video_id": "vid_123", "action": "create", "prompt": "Describe objects"}'

# Search
python scripts/scene_index.py '{"video_id": "vid_123", "action": "search", "query": "car"}'
```

## Common Errors

| Error | Solution |
|-------|----------|
| NOT_INDEXED | Create scene index first |
| VIDEO_NOT_FOUND | Check video ID |
| PROCESSING | Wait for indexing to complete |