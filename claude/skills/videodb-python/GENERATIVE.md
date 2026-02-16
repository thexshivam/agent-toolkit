# Generative Media Guide

VideoDB provides AI-powered generation of images, videos, audio, music, sound effects, and voice content.

## Image Generation

Generate images from text prompts:

```python
from videodb import GenerativeAIEngine

image = coll.generate_image(
    prompt="a futuristic cityscape at sunset with flying cars",
    engine=GenerativeAIEngine.DALLE3,
)

# Access the generated image
print(image.url)
```

**Available engines:**

| Engine | Description |
|--------|-------------|
| `GenerativeAIEngine.DALLE3` | OpenAI DALL-E 3 |
| `GenerativeAIEngine.STABILITY` | Stability AI |

## Video Generation

Generate short video clips from text prompts:

```python
video = coll.generate_video(
    prompt="a timelapse of a flower blooming in a garden",
    engine=GenerativeAIEngine.STABILITYAI_VIDEO,
)

stream_url = video.generate_stream()
video.play()
```

**Note:** Generated videos are automatically added to the collection and can be used in timelines, searches, and compilations like any uploaded video.

## Audio Generation

### Music

Generate background music from text descriptions:

```python
audio = coll.generate_audio(
    prompt="upbeat electronic music with a driving beat, suitable for a tech demo",
    engine=GenerativeAIEngine.ELEVENLABS_MUSIC,
    duration=30,  # seconds
)

print(audio.url)
```

### Sound Effects

Generate specific sound effects:

```python
sfx = coll.generate_audio(
    prompt="thunderstorm with heavy rain and distant thunder",
    engine=GenerativeAIEngine.ELEVENLABS_SFX,
    duration=10,
)
```

### Voice (Text-to-Speech)

Generate speech from text:

```python
voice = coll.generate_audio(
    prompt="Welcome to our product demo. Today we'll walk through the key features.",
    engine=GenerativeAIEngine.ELEVENLABS_TTS,
)
```

**Audio engine reference:**

| Engine | Type | Description |
|--------|------|-------------|
| `GenerativeAIEngine.ELEVENLABS_MUSIC` | Music | AI-generated music from prompts |
| `GenerativeAIEngine.ELEVENLABS_SFX` | SFX | Sound effect generation |
| `GenerativeAIEngine.ELEVENLABS_TTS` | Voice | Text-to-speech narration |

## Text Generation (LLM Integration)

Use language models to analyze video content:

```python
from videodb import TextGenerationEngine

# Generate text based on video content
response = video.generate_text(
    prompt="Summarize the key points discussed in this video",
    engine=TextGenerationEngine.OPENAI,
)

print(response.text)
```

**Text generation engines:**

| Engine | Description |
|--------|-------------|
| `TextGenerationEngine.OPENAI` | OpenAI GPT models |
| `TextGenerationEngine.ANTHROPIC` | Anthropic Claude models |

### Analyze Scenes with LLM

Combine scene extraction with text generation:

```python
# First extract scenes
scenes = video.index_scenes(
    extraction_type=SceneExtractionType.time_based,
    extraction_config={"time": 10},
)

# Then analyze with LLM
response = video.generate_text(
    prompt="Based on the visual content, describe the main topics covered",
    engine=TextGenerationEngine.OPENAI,
    scene_extraction_type=SceneExtractionType.time_based,
)
```

## Dubbing and Translation

Dub a video into another language:

```python
from videodb import DubbingEngine

dubbed_video = video.dub(
    target_language="es",  # Spanish
    engine=DubbingEngine.ELEVENLABS,
)

dubbed_video.play()
```

**Supported languages** include: `en`, `es`, `fr`, `de`, `it`, `pt`, `ja`, `ko`, `zh`, `hi`, `ar`, and more. Check VideoDB documentation for the full list.

## Common Patterns

### Generate Narration for a Video

```python
# Get transcript
transcript_text = video.get_transcript_text()

# Generate narration script
script = video.generate_text(
    prompt=f"Write a professional narration script for this video content: {transcript_text[:2000]}",
    engine=TextGenerationEngine.OPENAI,
)

# Convert script to speech
narration = coll.generate_audio(
    prompt=script.text,
    engine=GenerativeAIEngine.ELEVENLABS_TTS,
)
```

### Generate Thumbnail from Prompt

```python
# Generate a custom thumbnail image
thumbnail = coll.generate_image(
    prompt="professional video thumbnail showing data analytics dashboard, modern design",
    engine=GenerativeAIEngine.DALLE3,
)
```

### Add Generated Music to Video

```python
# Generate background music
music = coll.generate_audio(
    prompt="calm ambient background music for a tutorial video",
    engine=GenerativeAIEngine.ELEVENLABS_MUSIC,
    duration=60,
)

# Use in a timeline (see REFERENCE.md for timeline details)
from videodb import Timeline, VideoAsset, AudioAsset

timeline = Timeline(conn)
video_asset = VideoAsset(asset_id=video.id)
audio_asset = AudioAsset(asset_id=music.id)

timeline.add_inline(video_asset)
timeline.add_overlay(0, audio_asset)

stream_url = timeline.generate_stream()
```

## Tips

- **Generated media is persistent**: All generated content is stored in your collection and can be reused.
- **Combine generation types**: Generate images for overlays, music for backgrounds, and voice for narration, then combine using timelines.
- **Prompt quality matters**: Descriptive, specific prompts produce better results across all generation types.
- **Check quotas**: Generation operations consume API credits. Monitor usage via the VideoDB Console.
