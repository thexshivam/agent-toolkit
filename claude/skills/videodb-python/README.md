# VideoDB Python Skill for Claude Code

A Claude Code skill that enables AI-assisted video processing, search, editing, and generation using the [VideoDB](https://videodb.io) Python SDK.

## Overview

This skill gives Claude Code the ability to work with video as a first-class data type. Upload videos from URLs, YouTube, or local files, then search within them, generate transcripts, compose timelines, add subtitles, and create AI-generated media — all through natural language.

### Capabilities

- **Upload & Manage** — Ingest video, audio, and images from URLs, YouTube links, or local files
- **Search** — Semantic, keyword, and scene-based search across video content
- **Transcripts** — Generate and retrieve timestamped transcripts and full text
- **Timeline Editing** — Non-destructive multi-clip composition with text, image, and audio overlays
- **Subtitles** — Auto-generate and style subtitles from speech
- **AI Generation** — Create images, video clips, music, sound effects, and voiceovers from text prompts
- **Meeting Analysis** — Record meetings, extract transcripts, and generate summaries
- **Real-Time Streams** — Generate HLS stream URLs from videos, timelines, and search results

## Quick Start

### 1. Get an API Key

Sign up at [console.videodb.io](https://console.videodb.io) and copy your API key.

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your key:

```ini
VIDEO_DB_API_KEY=your-api-key-here
```

### 3. Set Up the Virtual Environment

```bash
python scripts/setup_venv.py
```

This creates a `.venv/` directory and installs all dependencies from `requirements.txt`.

### 4. Verify Connection

```bash
.venv/bin/python scripts/check_connection.py
```

## Project Structure

```text
videodb-python/
├── SKILL.md              # Skill definition (loaded by Claude Code)
├── REFERENCE.md          # Complete API reference
├── SEARCH.md             # Search and indexing guide
├── EDITOR.md             # Timeline editing guide
├── GENERATIVE.md         # AI generation guide
├── MEETINGS.md           # Meeting recording and analysis guide
├── RTSTREAM.md           # Real-time streaming guide
├── USE_CASES.md          # End-to-end workflow examples
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variable template
├── .gitignore
└── scripts/
    ├── setup_venv.py         # Virtual environment setup (idempotent)
    ├── setup.py              # Lightweight dependency checker
    ├── check_connection.py   # API key and connection verification
    ├── batch_upload.py       # Batch upload from URL list or file glob
    ├── search_and_compile.py # Search within video and compile results
    ├── extract_clips.py      # Extract clips by timestamp ranges
    ├── test_editor.py        # Integration tests for timeline editing
    ├── test_meetings.py      # Integration tests for meeting analysis
    └── test_rtstream.py      # Integration tests for streaming
```

## Usage Examples

### Upload and Search

```python
import videodb
from videodb import SearchType

conn = videodb.connect()
coll = conn.get_collection()

video = coll.upload(url="https://www.youtube.com/watch?v=VIDEO_ID")
video.index_spoken_words()

results = video.search("your query", search_type=SearchType.semantic)
results.play()
```

### Timeline Composition

```python
from videodb.timeline import Timeline
from videodb.asset import VideoAsset, TextAsset, TextStyle

timeline = Timeline(conn)
timeline.add_inline(VideoAsset(asset_id=video.id, start=10, end=30))
timeline.add_overlay(0, TextAsset(text="Title", duration=3, style=TextStyle(fontsize=36)))
stream_url = timeline.generate_stream()
```

### AI Generation

```python
image = coll.generate_image(prompt="sunset over mountains", aspect_ratio="16:9")
music = coll.generate_music(prompt="calm ambient background", duration=30)
voice = coll.generate_voice(text="Welcome to the demo.")
```

## Utility Scripts

| Script | Description |
|--------|-------------|
| `scripts/batch_upload.py` | Upload multiple files from a URL list or local directory |
| `scripts/search_and_compile.py` | Search within a video or collection and compile results |
| `scripts/extract_clips.py` | Extract clips at specific timestamp ranges |

```bash
# Batch upload from a text file of URLs
.venv/bin/python scripts/batch_upload.py --urls urls.txt --collection "My Project"

# Search and compile
.venv/bin/python scripts/search_and_compile.py --video-id <ID> --query "product demo"

# Extract clips
.venv/bin/python scripts/extract_clips.py --video-id <ID> --timestamps "10.0-25.0,45.0-60.0"
```

## Running Tests

The test scripts validate SDK operations against the live API:

```bash
.venv/bin/python scripts/test_editor.py
.venv/bin/python scripts/test_meetings.py
.venv/bin/python scripts/test_rtstream.py
```

Each test uploads a sample video, runs operations, verifies results, and cleans up.

## Documentation

| Guide | Contents |
|-------|----------|
| [SKILL.md](SKILL.md) | Skill definition and quick reference |
| [REFERENCE.md](REFERENCE.md) | Complete API reference for all objects and methods |
| [SEARCH.md](SEARCH.md) | Semantic, keyword, and scene-based search |
| [EDITOR.md](EDITOR.md) | Timeline editing with video, audio, image, and text assets |
| [GENERATIVE.md](GENERATIVE.md) | AI-generated images, video, music, sound effects, voice, and text |
| [MEETINGS.md](MEETINGS.md) | Meeting recording, transcription, and analysis |
| [RTSTREAM.md](RTSTREAM.md) | Real-time HLS streaming and live stream ingestion |
| [USE_CASES.md](USE_CASES.md) | End-to-end workflow examples |

## Requirements

- Python 3.9+
- [VideoDB Python SDK](https://github.com/video-db/videodb-python) v0.2.0+
- A VideoDB API key ([get one here](https://console.videodb.io))

## License

This skill is provided as-is for use with Claude Code. The VideoDB SDK is governed by its own [license](https://github.com/video-db/videodb-python/blob/main/LICENSE).
