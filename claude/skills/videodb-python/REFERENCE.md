# Complete API Reference

## Connection

```python
import videodb

conn = videodb.connect(
    api_key="your-api-key",      # or set VIDEO_DB_API_KEY env var
    base_url=None,                # custom API endpoint (optional)
)
```

**Returns:** `Connection` object

### Connection Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `conn.get_collection(collection_id="default")` | `Collection` | Get collection (default if no ID) |
| `conn.get_collections()` | `list[Collection]` | List all collections |
| `conn.create_collection(name, description, is_public=False)` | `Collection` | Create new collection |
| `conn.update_collection(id, name, description)` | `Collection` | Update a collection |
| `conn.check_usage()` | `dict` | Get account usage stats |
| `conn.upload(source, media_type, name, ...)` | `Video\|Audio\|Image` | Upload to default collection |
| `conn.record_meeting(meeting_url, bot_name, ...)` | `Meeting` | Record a meeting |
| `conn.youtube_search(query, result_threshold, duration)` | `list[dict]` | Search YouTube |
| `conn.transcode(source, callback_url, mode, ...)` | `str` | Transcode video (returns job ID) |
| `conn.connect_websocket(collection_id)` | `WebSocketConnection` | Connect to WebSocket service |

## Collections

```python
coll = conn.get_collection()
```

### Collection Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `coll.get_videos()` | `list[Video]` | List all videos |
| `coll.get_video(video_id)` | `Video` | Get specific video |
| `coll.get_audios()` | `list[Audio]` | List all audios |
| `coll.get_audio(audio_id)` | `Audio` | Get specific audio |
| `coll.get_images()` | `list[Image]` | List all images |
| `coll.get_image(image_id)` | `Image` | Get specific image |
| `coll.upload(url=None, file_path=None, media_type=None, name=None)` | `Video\|Audio\|Image` | Upload media |
| `coll.search(query, search_type, index_type=None)` | `SearchResult` | Search across collection |
| `coll.generate_image(prompt, aspect_ratio="1:1")` | `Image` | Generate image with AI |
| `coll.generate_video(prompt, duration=5)` | `Video` | Generate video with AI |
| `coll.generate_music(prompt, duration=5)` | `Audio` | Generate music with AI |
| `coll.generate_sound_effect(prompt, duration=2)` | `Audio` | Generate sound effect |
| `coll.generate_voice(text, voice_name="Default")` | `Audio` | Generate speech from text |
| `coll.generate_text(prompt, model_name="basic")` | `dict` | LLM text generation (result in `["output"]` key) |
| `coll.dub_video(video_id, language_code)` | `Video` | Dub video into another language |
| `coll.record_meeting(meeting_url, bot_name, ...)` | `Meeting` | Record a live meeting |
| `coll.connect_rtstream(url, name, ...)` | `RTStream` | Connect to a live stream |
| `coll.make_public()` | `None` | Make collection public |
| `coll.make_private()` | `None` | Make collection private |
| `coll.delete_video(video_id)` | `None` | Delete a video |
| `coll.delete_audio(audio_id)` | `None` | Delete an audio |
| `coll.delete_image(image_id)` | `None` | Delete an image |
| `coll.delete()` | `None` | Delete the collection |

### Upload Parameters

```python
video = coll.upload(
    url=None,            # Remote URL (HTTP, YouTube)
    file_path=None,      # Local file path
    media_type=None,     # "video", "audio", or "image" (auto-detected if omitted)
    name=None,           # Custom name for the media
    description=None,    # Description
    callback_url=None,   # Webhook URL for async notification
)
```

## Video Object

```python
video = coll.get_video(video_id)
```

### Video Properties

| Property | Type | Description |
|----------|------|-------------|
| `video.id` | `str` | Unique video ID |
| `video.collection_id` | `str` | Parent collection ID |
| `video.name` | `str` | Video name |
| `video.description` | `str` | Video description |
| `video.length` | `float` | Duration in seconds |
| `video.stream_url` | `str` | Default stream URL |
| `video.player_url` | `str` | Player embed URL |
| `video.thumbnail_url` | `str` | Thumbnail URL |

### Video Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `video.generate_stream(timeline=None)` | `str` | Generate stream URL (optional timeline of `[(start, end)]` tuples) |
| `video.play()` | `str` | Open stream in browser, returns player URL |
| `video.index_spoken_words(language_code=None)` | `None` | Index speech for search |
| `video.index_scenes(extraction_type, prompt, extraction_config={})` | `str` | Index visual scenes (returns scene_index_id) |
| `video.index_visuals(prompt, batch_config, ...)` | `str` | Index visuals (returns scene_index_id) |
| `video.index_audio(prompt, model_name, ...)` | `str` | Index audio with LLM (returns scene_index_id) |
| `video.get_transcript(start=None, end=None)` | `list[dict]` | Get timestamped transcript |
| `video.get_transcript_text(start=None, end=None)` | `str` | Get full transcript text |
| `video.generate_transcript(force=None)` | `str` | Generate transcript |
| `video.translate_transcript(language, additional_notes)` | `list[dict]` | Translate transcript |
| `video.search(query, search_type=SearchType.semantic)` | `SearchResult` | Search within video |
| `video.add_subtitle(style=SubtitleStyle())` | `str` | Add subtitles (returns stream URL) |
| `video.generate_thumbnail(time=None)` | `str\|Image` | Generate thumbnail |
| `video.get_thumbnails()` | `list[Image]` | Get all thumbnails |
| `video.extract_scenes(extraction_type, extraction_config)` | `SceneCollection` | Extract scenes |
| `video.reframe(start, end, target, mode)` | `Video` | Reframe video aspect ratio |
| `video.clip(prompt, content_type, model_name)` | `SearchResult` | Generate clip from prompt |
| `video.insert_video(video, timestamp)` | `str` | Insert video at timestamp |
| `video.download(name=None)` | `dict` | Download the video |
| `video.delete()` | `None` | Delete the video |

## Audio Object

```python
audio = coll.get_audio(audio_id)
```

### Audio Properties

| Property | Type | Description |
|----------|------|-------------|
| `audio.id` | `str` | Unique audio ID |
| `audio.collection_id` | `str` | Parent collection ID |
| `audio.name` | `str` | Audio name |
| `audio.length` | `float` | Duration in seconds |

### Audio Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `audio.generate_url()` | `str` | Generate signed URL for playback |
| `audio.get_transcript(start=None, end=None)` | `list[dict]` | Get timestamped transcript |
| `audio.get_transcript_text(start=None, end=None)` | `str` | Get full transcript text |
| `audio.generate_transcript(force=None)` | `dict` | Generate transcript |
| `audio.delete()` | `None` | Delete the audio |

## Image Object

```python
image = coll.get_image(image_id)
```

### Image Properties

| Property | Type | Description |
|----------|------|-------------|
| `image.id` | `str` | Unique image ID |
| `image.collection_id` | `str` | Parent collection ID |
| `image.name` | `str` | Image name |

### Image Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `image.generate_url()` | `str` | Generate signed URL |
| `image.delete()` | `None` | Delete the image |

## Timeline & Editor

### Timeline

```python
from videodb.timeline import Timeline

timeline = Timeline(conn)
```

| Method | Returns | Description |
|--------|---------|-------------|
| `timeline.add_inline(asset)` | `None` | Add `VideoAsset` sequentially on main track |
| `timeline.add_overlay(start, asset)` | `None` | Overlay `AudioAsset`, `ImageAsset`, or `TextAsset` at timestamp |
| `timeline.generate_stream()` | `str` | Compile and get stream URL |

### Asset Types

#### VideoAsset

```python
from videodb.asset import VideoAsset

asset = VideoAsset(
    asset_id=video.id,
    start=0,              # trim start (seconds)
    end=None,             # trim end (seconds, None = full)
)
```

#### AudioAsset

```python
from videodb.asset import AudioAsset

asset = AudioAsset(
    asset_id=audio.id,
    start=0,
    end=None,
    disable_other_tracks=True,   # mute original audio when True
    fade_in_duration=0,          # seconds (max 5)
    fade_out_duration=0,         # seconds (max 5)
)
```

#### ImageAsset

```python
from videodb.asset import ImageAsset

asset = ImageAsset(
    asset_id=image.id,
    duration=None,        # display duration (seconds)
    width=100,            # display width
    height=100,           # display height
    x=80,                 # horizontal position (px from left)
    y=20,                 # vertical position (px from top)
)
```

#### TextAsset

```python
from videodb.asset import TextAsset, TextStyle

asset = TextAsset(
    text="Hello World",
    duration=5,
    style=TextStyle(
        fontsize=24,
        fontcolor="black",
        boxcolor="white",       # background box colour
        alpha=1.0,
        font="Sans",
        text_align="T",         # text alignment within box
    ),
)
```

#### CaptionAsset (Editor API)

CaptionAsset belongs to the Editor API, which has its own Timeline, Track, and Clip system:

```python
from videodb.editor import CaptionAsset, FontStyling

asset = CaptionAsset(
    src="auto",                    # "auto" or base64 ASS string
    font=FontStyling(name="Clear Sans", size=30),
    primary_color="&H00FFFFFF",
)
```

See [EDITOR.md](EDITOR.md#caption-overlays) for full CaptionAsset usage with the Editor API.

## SearchResult Object

```python
results = video.search("query", search_type=SearchType.semantic)
```

| Method | Returns | Description |
|--------|---------|-------------|
| `results.get_shots()` | `list[Shot]` | Get list of matching segments |
| `results.compile()` | `str` | Compile all shots into a stream URL |
| `results.play()` | `str` | Open compiled stream in browser |

### Shot Properties

| Property | Type | Description |
|----------|------|-------------|
| `shot.video_id` | `str` | Source video ID |
| `shot.video_length` | `float` | Source video duration |
| `shot.video_title` | `str` | Source video title |
| `shot.start` | `float` | Start time (seconds) |
| `shot.end` | `float` | End time (seconds) |
| `shot.text` | `str` | Matched text content |
| `shot.search_score` | `float` | Search relevance score |

| Method | Returns | Description |
|--------|---------|-------------|
| `shot.generate_stream()` | `str` | Stream this specific shot |
| `shot.play()` | `str` | Open shot stream in browser |

## Meeting Object

```python
meeting = coll.record_meeting(meeting_url="https://meet.google.com/...", bot_name="Bot")
```

### Meeting Properties

| Property | Type | Description |
|----------|------|-------------|
| `meeting.id` | `str` | Unique meeting ID |
| `meeting.collection_id` | `str` | Parent collection ID |
| `meeting.status` | `str` | Current status |
| `meeting.video_id` | `str` | Recorded video ID (after completion) |
| `meeting.bot_name` | `str` | Bot name |
| `meeting.meeting_title` | `str` | Meeting title |
| `meeting.meeting_url` | `str` | Meeting URL |
| `meeting.speaker_timeline` | `dict` | Speaker timeline data |
| `meeting.is_active` | `bool` | True if initializing or processing |
| `meeting.is_completed` | `bool` | True if done |

### Meeting Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `meeting.refresh()` | `Meeting` | Refresh data from server |
| `meeting.wait_for_status(target_status, timeout=14400, interval=120)` | `bool` | Poll until status reached |

## RTStream Object

```python
rtstream = coll.connect_rtstream(url="rtmp://...", name="My Stream")
```

### RTStream Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `rtstream.start()` | `None` | Begin ingestion |
| `rtstream.stop()` | `None` | Stop ingestion |
| `rtstream.generate_stream(start, end)` | `str` | Stream recorded segment (Unix timestamps) |
| `rtstream.export(name=None)` | `RTStreamExportResult` | Export to permanent video |
| `rtstream.index_scenes(extraction_type, ...)` | `RTStreamSceneIndex` | Index visual scenes |
| `rtstream.index_spoken_words(prompt, ...)` | `RTStreamSceneIndex` | Index spoken words |
| `rtstream.search(query, index_id=None, ...)` | `RTStreamSearchResult` | Search recorded content |
| `rtstream.start_transcript(ws_connection_id)` | `dict` | Start live transcription |
| `rtstream.get_transcript(page, page_size)` | `dict` | Get transcript pages |
| `rtstream.stop_transcript()` | `dict` | Stop transcription |

## Enums & Constants

### SearchType

```python
from videodb import SearchType

SearchType.semantic    # Natural language semantic search
SearchType.keyword     # Exact keyword matching
# Note: SearchType.scene is not currently supported by the API.
# Use SearchType.semantic after index_scenes() to search visual content.
```

### SceneExtractionType

```python
from videodb import SceneExtractionType

SceneExtractionType.shot_based   # Automatic shot boundary detection
SceneExtractionType.time_based   # Fixed time interval extraction
```

### SubtitleStyle

```python
from videodb import SubtitleStyle

style = SubtitleStyle(
    font_name="Arial",
    font_size=18,
    primary_colour="&H00FFFFFF",
    bold=False,
    # ... see SubtitleStyle for all options
)
video.add_subtitle(style=style)
```

### SubtitleAlignment & SubtitleBorderStyle

```python
from videodb import SubtitleAlignment, SubtitleBorderStyle
```

### TextStyle

```python
from videodb import TextStyle
# or: from videodb.asset import TextStyle

style = TextStyle(
    fontsize=24,
    fontcolor="black",
    boxcolor="white",
    font="Sans",
    text_align="T",
    alpha=1.0,
)
```

### Other Constants

```python
from videodb import (
    IndexType,          # spoken_word, scene
    MediaType,          # video, audio, image
    Segmenter,          # word, sentence, time
    SegmentationType,   # sentence, word
    TranscodeMode,      # economy, standard
    ResizeMode,         # crop, pad, stretch
    ReframeMode,        # simple, smart
    RTStreamChannelType,
)
```

## Exceptions

```python
from videodb.exceptions import (
    AuthenticationError,     # Invalid or missing API key
    InvalidRequestError,     # Bad parameters or malformed request
    RequestTimeoutError,     # Request timed out
    SearchError,             # Search operation failure (e.g. not indexed)
    VideodbError,            # Base exception for all VideoDB errors
)
```

| Exception | Common Cause |
|-----------|-------------|
| `AuthenticationError` | Missing or invalid `VIDEO_DB_API_KEY` |
| `InvalidRequestError` | Invalid URL, unsupported format, bad parameters |
| `RequestTimeoutError` | Server took too long to respond |
| `SearchError` | Searching before indexing, invalid search type |
| `VideodbError` | Server errors, network issues, generic failures |
