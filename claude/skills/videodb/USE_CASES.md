# Real-World Use Cases

End-to-end workflows demonstrating common VideoDB operations.

## Create Video Highlight Reel

Upload a long video, search for key moments, and compile them into a highlight reel:

```python
import videodb
from videodb import SearchType
from videodb.timeline import Timeline
from videodb.asset import VideoAsset

conn = videodb.connect()
coll = conn.get_collection()

# 1. Upload the full video
video = coll.upload(url="https://example.com/conference-talk.mp4")

# 2. Index spoken content
video.index_spoken_words()

# 3. Search for key topics
topics = [
    "announcing the new product",
    "live demo of the feature",
    "audience Q&A session",
]

all_shots = []
for topic in topics:
    results = video.search(topic, search_type=SearchType.semantic)
    all_shots.extend(results.get_shots())

# 4. Build a timeline from the shots
timeline = Timeline(conn)
for shot in all_shots:
    asset = VideoAsset(asset_id=shot.video_id, start=shot.start, end=shot.end)
    timeline.add_inline(asset)

# 5. Generate and share
stream_url = timeline.generate_stream()
print(f"Highlight reel: {stream_url}")
```

## Build a Searchable Video Library

Batch upload, index, and enable cross-collection search:

```python
import videodb

conn = videodb.connect()
coll = conn.create_collection(name="Training Videos", description="Internal training library")

# 1. Upload multiple videos
urls = [
    "https://example.com/onboarding-part1.mp4",
    "https://example.com/onboarding-part2.mp4",
    "https://example.com/security-training.mp4",
]

videos = []
for url in urls:
    video = coll.upload(url=url)
    videos.append(video)
    print(f"Uploaded: {video.name} ({video.id})")

# 2. Index all videos
for video in videos:
    video.index_spoken_words()
    print(f"Indexed: {video.name}")

# 3. Search across the entire collection
results = coll.search(
    query="how to reset your password",
    search_type=videodb.SearchType.semantic,
)

for shot in results.get_shots():
    print(f"Found in {shot.video_id}: [{shot.start:.1f}s - {shot.end:.1f}s]")

# 4. Play compiled results
results.play()
```

Or use the helper script:

```bash
python scripts/batch_upload.py --urls urls.txt --collection "Training Videos"
```

## Add Professional Polish to Raw Footage

Upload raw footage, add subtitles, and generate a thumbnail:

```python
import videodb

conn = videodb.connect()
coll = conn.get_collection()

# 1. Upload raw footage
video = coll.upload(file_path="/path/to/raw-footage.mp4")

# 2. Generate transcript
video.index_spoken_words()
transcript = video.get_transcript_text()
print(f"Transcript ({len(transcript)} chars): {transcript[:200]}...")

# 3. Add auto-subtitles
stream_url = video.add_subtitle()

# 4. Generate thumbnail
thumbnail = video.generate_thumbnail(time=15.0)

print(f"Stream with subtitles: {stream_url}")
```

## Search and Extract Specific Clips

Find moments and download them as individual clips:

```python
import videodb
from videodb import SearchType

conn = videodb.connect()
coll = conn.get_collection()
video = coll.get_video("your-video-id")

# 1. Index if not already done
video.index_spoken_words()

# 2. Search for a specific topic
results = video.search("budget discussion", search_type=SearchType.semantic)

# 3. Extract each matching clip
shots = results.get_shots()
print(f"Found {len(shots)} matching segments")

for i, shot in enumerate(shots):
    stream_url = shot.generate_stream()
    print(f"Clip {i+1}: {shot.start:.1f}s - {shot.end:.1f}s -> {stream_url}")
```

Or use the helper script:

```bash
python scripts/extract_clips.py --video-id <id> --timestamps "10.0-25.0,45.0-60.0,120.0-135.0"
```

## Generate AI-Enhanced Video Content

Combine generative AI with existing video:

```python
import videodb
from videodb.timeline import Timeline
from videodb.asset import VideoAsset, AudioAsset, ImageAsset

conn = videodb.connect()
coll = conn.get_collection()
video = coll.get_video("your-video-id")

# 1. Generate a summary of the video
video.index_spoken_words()
transcript_text = video.get_transcript_text()
result = coll.generate_text(
    prompt=f"Create a concise 2-sentence summary of this video:\n{transcript_text}",
    model_name="pro",
)
print(f"Summary: {result['output']}")

# 2. Generate background music
music = coll.generate_music(
    prompt="calm corporate background music, professional and modern",
    duration=int(video.length),
)

# 3. Generate intro image
intro = coll.generate_image(
    prompt="modern professional title card with abstract tech background",
    aspect_ratio="16:9",
)

# 4. Combine into a polished timeline
timeline = Timeline(conn)

# Add the main video
timeline.add_inline(VideoAsset(asset_id=video.id))

# Overlay intro image for first 5 seconds
timeline.add_overlay(0, ImageAsset(asset_id=intro.id, duration=5, width=1280, height=720, x=0, y=0))

# Overlay background music (mixed with original audio)
timeline.add_overlay(0, AudioAsset(asset_id=music.id, disable_other_tracks=False))

# 5. Generate final stream
stream_url = timeline.generate_stream()
print(f"Enhanced video: {stream_url}")
```
