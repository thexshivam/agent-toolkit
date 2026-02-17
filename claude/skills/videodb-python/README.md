# VideoDB Skill for Claude Code

Talk to your videos using Claude Code. Upload, search, edit, generate subtitles, create clips — all with natural language.

## What Can It Do?

- **Upload** videos from YouTube, URLs, or your local files
- **Search** inside videos by what was said or what was shown
- **Transcripts** — get timestamped text from any video
- **Edit** — combine clips, add text/image/audio overlays
- **Subtitles** — auto-generate and style them
- **AI Generate** — create images, video, music, voiceovers from text
- **Meetings** — upload recordings, get summaries and action items
- **Stream** — get playable HLS links for anything you build

---

## Setup (First Time Only)

### Step 1: Clone the repo

```bash
git clone https://github.com/video-db/agent-toolkit.git
```

### Step 2: Get your API key

Go to [console.videodb.io](https://console.videodb.io), sign up, and copy your API key.

### Step 3: Add your API key

Go into the skill folder and create a `.env` file:

```bash
cd agent-toolkit/claude/skills/videodb-python
cp .env.example .env
```

Open `.env` and paste your key:

```
VIDEO_DB_API_KEY=your-api-key-here
```

### Step 4: Tell Claude Code where the skill is

Open Claude Code and add the path to the skill folder:

```
/add-dir /path/to/agent-toolkit/claude/skills/videodb-python
```

Replace `/path/to/` with the actual path on your machine.

### Step 5: Use it for the first time

Just type `/videodb-python` followed by any task. On the first run, Claude Code will automatically set up the environment and install everything.

```
/videodb-python upload this YouTube video and give me a transcript
```

That's it. Setup is done.

---

## After Setup

Once it's set up, you don't need to do anything special. Just use `/videodb-python` and ask for what you want. The skill handles the rest.

### Examples

```
/videodb-python upload https://www.youtube.com/watch?v=VIDEO_ID and search for "product demo"
```

```
/videodb-python add subtitles to my latest video
```

```
/videodb-python generate a 30 second background music track
```

```
/videodb-python summarize this meeting recording with action items
```

```
/videodb-python take clips from 10s-30s and 45s-60s and combine them
```

---

## Utility Scripts

These are helper scripts you can also run directly if needed:

| Script | What it does |
|--------|-------------|
| `scripts/setup_venv.py` | Sets up Python environment (runs automatically) |
| `scripts/check_connection.py` | Tests if your API key works |
| `scripts/batch_upload.py` | Upload many files at once |
| `scripts/search_and_compile.py` | Search inside a video and compile results |
| `scripts/extract_clips.py` | Cut out clips by timestamps |

---

## Guides

Want to go deeper? Check these out:

| Guide | What's inside |
|-------|----------|
| [REFERENCE.md](REFERENCE.md) | Full API reference |
| [SEARCH.md](SEARCH.md) | Search and indexing |
| [EDITOR.md](EDITOR.md) | Timeline editing |
| [GENERATIVE.md](GENERATIVE.md) | AI-generated media |
| [MEETINGS.md](MEETINGS.md) | Meeting analysis |
| [RTSTREAM.md](RTSTREAM.md) | Real-time streaming |
| [USE_CASES.md](USE_CASES.md) | Full workflow examples |

## Requirements

- Python 3.9 or higher
- A VideoDB API key — [get one here](https://console.videodb.io)

## License

This skill is provided as-is for use with Claude Code. The VideoDB SDK is governed by its own [license](https://github.com/video-db/videodb-python/blob/main/LICENSE).
