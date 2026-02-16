---
name: videodb-python
description: Process videos using VideoDB Python SDK. Upload local files, URLs, or YouTube videos. Transcode, add subtitles, generate transcripts and thumbnails, search within videos, and create video compilations. Use for Python projects working with video processing, video search, or video editing.
allowed-tools: Read Grep Glob Bash(python:*)
argument-hint: "[task description]"
---

# VideoDB Python SDK

## Prerequisites

Before using any VideoDB operations, ensure the environment is ready:

```bash
python scripts/setup_venv.py
python scripts/check_connection.py
```

If `videodb` is not installed or the virtual environment is missing, run `scripts/setup_venv.py` first. It will create a `.venv/` and install all dependencies from `requirements.txt`.

## Setup

### API Key

An API key from [VideoDB Console](https://console.videodb.io) is required.

```python
import videodb

# Option 1: .env file (recommended)
# Copy .env.example to .env and fill in your key:
#   cp .env.example .env
# All scripts automatically load from .env via python-dotenv.
conn = videodb.connect()

# Option 2: Environment variable
# export VIDEO_DB_API_KEY="your-api-key"
conn = videodb.connect()

# Option 3: Pass directly
conn = videodb.connect(api_key="your-api-key")
```

If the `VIDEO_DB_API_KEY` environment variable is not set and no key is passed, prompt the user for it.

### Connection Object

The connection object is the entry point to all VideoDB operations:

```python
conn = videodb.connect()
coll = conn.get_collection()  # default collection
```

## Quick Reference

### Upload Media

```python
# Upload from URL
video = coll.upload(url="https://example.com/video.mp4")

# Upload from YouTube
video = coll.upload(url="https://www.youtube.com/watch?v=VIDEO_ID")

# Upload local file
video = coll.upload(file_path="/path/to/video.mp4")

# Upload audio
audio = coll.upload(url="https://example.com/audio.mp3", media_type="audio")

# Upload image
image = coll.upload(url="https://example.com/image.jpg", media_type="image")
```

### Get Stream Link

```python
video = coll.get_video(video_id)
stream_url = video.generate_stream()
video.play()  # opens in browser
```

### Add Subtitles

```python
from videodb import SubtitleStyle

# Auto-generate subtitles from transcript
video.index_spoken_words()
stream_url = video.add_subtitle()

# With custom styling
stream_url = video.add_subtitle(style=SubtitleStyle(font_size=22))
```

### Transcripts

```python
# Generate transcript (must be done before text search)
video.index_spoken_words()

# Get transcript
transcript = video.get_transcript()
for entry in transcript:
    print(f"[{entry['start']:.1f}s - {entry['end']:.1f}s] {entry['text']}")

# Get full text
text = video.get_transcript_text()
```

### Thumbnails

```python
# Generate thumbnail at a specific timestamp
thumbnail = video.generate_thumbnail(time=10.5)
```

## Error Handling

```python
from videodb.exceptions import (
    AuthenticationError,   # Invalid or missing API key
    InvalidRequestError,   # Bad request parameters
    SearchError,           # Search operation failures
)

try:
    conn = videodb.connect()
except AuthenticationError:
    print("Check your VIDEO_DB_API_KEY")

try:
    video = coll.upload(url=url)
except InvalidRequestError as e:
    print(f"Upload failed: {e}")
```

## Search Inside Videos

Index and search video content by spoken words or visual scenes.

### Quick Start

```python
video.index_spoken_words()
results = video.search("your query")
results.play()  # streams compiled matches
```

See [SEARCH.md](SEARCH.md) for the complete search and indexing guide.

## Generative Media

Create AI-generated images, videos, music, sound effects, voice, and text content.

### Quick Start

```python
image = coll.generate_image(
    prompt="a sunset over mountains",
    aspect_ratio="16:9",
)
```

See [GENERATIVE.md](GENERATIVE.md) for the complete AI generation guide.

## Collections

Organize media at scale using collections.

```python
# List all collections
collections = conn.get_collections()

# Create a new collection
coll = conn.create_collection(name="My Project", description="Project videos")

# Get specific collection
coll = conn.get_collection(collection_id)

# List videos in collection
videos = coll.get_videos()
```

See [REFERENCE.md](REFERENCE.md#collections) for complete collection management.

## Timeline Editing

Compose videos from multiple clips, add text/image/audio overlays, and trim segments — all non-destructive.

### Quick Start

```python
from videodb.timeline import Timeline
from videodb.asset import VideoAsset, TextAsset, TextStyle

timeline = Timeline(conn)
timeline.add_inline(VideoAsset(asset_id=video.id, start=10, end=30))
timeline.add_overlay(0, TextAsset(text="The End", duration=3, style=TextStyle(fontsize=36)))
stream_url = timeline.generate_stream()
```

See [EDITOR.md](EDITOR.md) for the complete timeline editing guide.

## Meeting Recording Analysis

Process meeting recordings to extract transcripts, generate summaries, identify action items and decisions.

### Quick Start

```python
meeting.index_spoken_words()
text = meeting.get_transcript_text()

summary = coll.generate_text(
    prompt=f"Summarize this meeting with action items and decisions:\n{text}",
    model_name="pro",
)
print(summary)
```

See [MEETINGS.md](MEETINGS.md) for the complete meeting recording guide.

## Real-Time Streams

Generate streamable HLS URLs from videos, timelines, and search results for live playback.

### Quick Start

```python
stream_url = video.generate_stream()
# Or from a timeline composition
stream_url = timeline.generate_stream()
# Or from search results
stream_url = results.compile()
```

See [RTSTREAM.md](RTSTREAM.md) for the complete real-time streams guide.

## Next Steps

For advanced features, see:
- [SEARCH.md](SEARCH.md) - Search and indexing (semantic, keyword, scene-based)
- [EDITOR.md](EDITOR.md) - Timeline editing (overlays, trim, multi-clip composition)
- [MEETINGS.md](MEETINGS.md) - Meeting analysis (transcripts, summaries, action items)
- [RTSTREAM.md](RTSTREAM.md) - Real-time streams (HLS, dynamic composition, playback)
- [GENERATIVE.md](GENERATIVE.md) - AI-generated media (images, video, audio, voice)
- [REFERENCE.md](REFERENCE.md) - Complete API reference
- [USE_CASES.md](USE_CASES.md) - End-to-end workflow examples
