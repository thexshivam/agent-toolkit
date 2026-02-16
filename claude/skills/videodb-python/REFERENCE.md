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
| `conn.get_collection(collection_id=None)` | `Collection` | Get collection (default if no ID) |
| `conn.get_collections()` | `list[Collection]` | List all collections |
| `conn.create_collection(name, description="")` | `Collection` | Create new collection |
| `conn.delete_collection(collection_id)` | `None` | Delete a collection |
| `conn.get_usage()` | `dict` | Get account usage stats |

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
| `coll.generate_image(prompt, engine)` | `Image` | Generate image with AI |
| `coll.generate_video(prompt, engine)` | `Video` | Generate video with AI |
| `coll.generate_audio(prompt, engine, duration=None)` | `Audio` | Generate audio with AI |
| `coll.delete_video(video_id)` | `None` | Delete a video |
| `coll.delete_audio(audio_id)` | `None` | Delete an audio |
| `coll.delete_image(image_id)` | `None` | Delete an image |

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
| `video.name` | `str` | Video name |
| `video.length` | `float` | Duration in seconds |
| `video.stream_url` | `str` | Default stream URL |
| `video.player_url` | `str` | Player embed URL |
| `video.thumbnail_url` | `str` | Thumbnail URL |
| `video.collection_id` | `str` | Parent collection ID |

### Video Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `video.generate_stream(timeline=None, resolution=None)` | `str` | Generate stream URL |
| `video.play()` | `None` | Open stream in browser |
| `video.index_spoken_words()` | `None` | Index speech for search |
| `video.index_scenes(extraction_type, prompt, extraction_config=None)` | `None` | Index visual scenes |
| `video.get_transcript()` | `list[dict]` | Get timestamped transcript |
| `video.get_transcript_text()` | `str` | Get full transcript text |
| `video.search(query, search_type=SearchType.semantic)` | `SearchResult` | Search within video |
| `video.add_subtitle()` | `None` | Auto-generate subtitles |
| `video.generate_thumbnail(time=None)` | `str \| Image` | Generate thumbnail |
| `video.generate_text(prompt, engine, scene_extraction_type=None)` | `TextGenerationResult` | LLM analysis |
| `video.dub(target_language, engine)` | `Video` | Dub into another language |
| `video.delete()` | `None` | Delete the video |

## Audio Object

```python
audio = coll.get_audio(audio_id)
```

### Audio Properties

| Property | Type | Description |
|----------|------|-------------|
| `audio.id` | `str` | Unique audio ID |
| `audio.name` | `str` | Audio name |
| `audio.length` | `float` | Duration in seconds |
| `audio.url` | `str` | Audio URL |

### Audio Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `audio.generate_stream()` | `str` | Generate stream URL |
| `audio.play()` | `None` | Open stream in browser |
| `audio.delete()` | `None` | Delete the audio |

## Image Object

```python
image = coll.get_image(image_id)
```

### Image Properties

| Property | Type | Description |
|----------|------|-------------|
| `image.id` | `str` | Unique image ID |
| `image.name` | `str` | Image name |
| `image.url` | `str` | Image URL |

### Image Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `image.generate_stream()` | `str` | Generate stream URL |
| `image.delete()` | `None` | Delete the image |

## Timeline & Editor

### Timeline

```python
from videodb import Timeline

timeline = Timeline(conn)
```

| Method | Returns | Description |
|--------|---------|-------------|
| `timeline.add_inline(asset)` | `None` | Add asset sequentially on main track |
| `timeline.add_overlay(start, asset)` | `None` | Overlay asset at timestamp |
| `timeline.generate_stream()` | `str` | Compile and get stream URL |
| `timeline.play()` | `None` | Open compiled stream in browser |

### Asset Types

#### VideoAsset

```python
from videodb import VideoAsset

asset = VideoAsset(
    asset_id=video.id,
    start=0,              # trim start (seconds)
    end=None,             # trim end (seconds, None = full)
    volume=1.0,           # 0.0 to 1.0
)
```

#### AudioAsset

```python
from videodb import AudioAsset

asset = AudioAsset(
    asset_id=audio.id,
    start=0,
    end=None,
    volume=0.8,
    fade_in_duration=0,   # seconds
    fade_out_duration=0,  # seconds
)
```

#### ImageAsset

```python
from videodb import ImageAsset

asset = ImageAsset(
    asset_id=image.id,
    duration=5,           # display duration (seconds)
    width=None,
    height=None,
    x=0,                  # horizontal position
    y=0,                  # vertical position
    opacity=1.0,          # 0.0 to 1.0
)
```

#### TextAsset

```python
from videodb import TextAsset, TextStyle

asset = TextAsset(
    text="Hello World",
    duration=5,
    style=TextStyle(
        fontsize=24,
        fontcolor="white",
        bgcolor="black",
        alpha=1.0,
        font="Arial",
        alignment="center",  # "left", "center", "right"
    ),
)
```

#### CaptionAsset

```python
from videodb import CaptionAsset

asset = CaptionAsset(
    asset_id=video.id,    # video with indexed transcript
)
```

## Enums & Constants

### SearchType

```python
from videodb import SearchType

SearchType.semantic    # Natural language semantic search
SearchType.keyword     # Exact keyword matching
SearchType.scene       # Visual scene search
```

### SceneExtractionType

```python
from videodb import SceneExtractionType

SceneExtractionType.shot_based   # Automatic shot boundary detection
SceneExtractionType.time_based   # Fixed time interval extraction
```

### MediaResolution

```python
from videodb import MediaResolution

MediaResolution.R_360p
MediaResolution.R_480p
MediaResolution.R_720p
MediaResolution.R_1080p
```

### GenerativeAIEngine

```python
from videodb import GenerativeAIEngine

# Image
GenerativeAIEngine.DALLE3
GenerativeAIEngine.STABILITY

# Video
GenerativeAIEngine.STABILITYAI_VIDEO

# Audio
GenerativeAIEngine.ELEVENLABS_MUSIC
GenerativeAIEngine.ELEVENLABS_SFX
GenerativeAIEngine.ELEVENLABS_TTS
```

### TextGenerationEngine

```python
from videodb import TextGenerationEngine

TextGenerationEngine.OPENAI
TextGenerationEngine.ANTHROPIC
```

### DubbingEngine

```python
from videodb import DubbingEngine

DubbingEngine.ELEVENLABS
```

## Exceptions

```python
from videodb.exceptions import (
    AuthenticationError,     # Invalid or missing API key
    InvalidRequestError,     # Bad parameters or malformed request
    SearchError,             # Search operation failure (e.g. not indexed)
    VideodbError,            # Base exception for all VideoDB errors
)
```

| Exception | Common Cause |
|-----------|-------------|
| `AuthenticationError` | Missing or invalid `VIDEO_DB_API_KEY` |
| `InvalidRequestError` | Invalid URL, unsupported format, bad parameters |
| `SearchError` | Searching before indexing, invalid search type |
| `VideodbError` | Server errors, network issues, generic failures |
