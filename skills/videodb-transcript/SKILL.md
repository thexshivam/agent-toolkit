---
name: videodb-transcript
description: Get and analyze video transcriptions from VideoDB. Use this skill when users want to read transcripts, summarize video content, or analyze what was said in videos. Supports multiple languages and provides timestamped text. Triggers on "transcript", "what was said", "summarize video", "transcribe".
---

# VideoDB Transcript

Extract, read, and analyze spoken content from videos with automatic transcription.

## Quick Start

```python
from videodb import connect

conn = connect()
video = conn.get_collection().get_video("video_id")

# Get transcript with timestamps
transcript = video.get_transcript()

# Get plain text only
text = video.get_transcript_text()
```

## When to Use

- User asks for "transcript" or "transcription"
- User wants to "summarize" video content
- User asks "what was said" in a video
- User needs text for analysis or processing

## Core Functions

### Get Timestamped Transcript
```python
transcript = video.get_transcript()
# Returns: [{"start": 0.0, "end": 3.5, "text": "Hello everyone"}, ...]
```

### Get Plain Text
```python
text = video.get_transcript_text()
# Returns: "Hello everyone. Welcome to..."
```

### Force Regeneration
```python
transcript = video.get_transcript(force=True)
```

## Adding Subtitles

```python
# Get video stream with burned-in subtitles
stream_url = video.add_subtitle()
```

## Working with Transcripts

```python
transcript = video.get_transcript()

# Iterate through segments
for segment in transcript:
    print(f"[{segment['start']:.1f}s] {segment['text']}")

# Find specific content
pricing_parts = [s for s in transcript if "pricing" in s["text"].lower()]
```

## Language Support

VideoDB auto-detects language. Supported languages include:
- English (en), Spanish (es), French (fr), German (de)
- Hindi (hi), Chinese (zh), Japanese (ja), Korean (ko)
- And 40+ more languages

## Processing Time

| Video Length | Time |
|--------------|------|
| < 5 min | ~30 seconds |
| 5-30 min | 1-3 minutes |
| 30-60 min | 3-5 minutes |

**Note:** Transcripts are generated automatically on first request. If you get `NO_TRANSCRIPT` error, the video may still be processing - wait and retry.

## Scripts

Run `scripts/transcript.py` for programmatic access:
```bash
python scripts/transcript.py '{"video_id": "vid_123"}'
python scripts/transcript.py '{"video_id": "vid_123", "format": "text"}'
```

## Common Errors

| Error | Solution |
|-------|----------|
| VIDEO_NOT_FOUND | Check video ID |
| NO_TRANSCRIPT | Video may still be processing, wait and retry |
| NO_AUDIO | Video has no audio track |