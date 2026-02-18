# VideoDB Agent Skill for Claude

Talk to your videos using natural language. Upload, search, edit, generate subtitles, create clips, and more.

> Built on the [VideoDB Python SDK](https://github.com/video-db/videodb-python) | Works with **Claude Code**, **Claude Web**, and the **Claude API**

---

## What You Can Do

| Capability | Description |
|---|---|
| **Upload** | Ingest videos from YouTube, URLs, or local files |
| **Search** | Find moments by what was said (speech) or what was shown (scenes) |
| **Transcripts** | Generate timestamped transcripts from any video |
| **Edit** | Combine clips, trim, add text/image/audio overlays |
| **Subtitles** | Auto-generate and style subtitles |
| **AI Generate** | Create images, video, music, sound effects, and voiceovers from text |
| **Meetings** | Record meetings, extract transcripts, get summaries and action items |
| **Stream** | Get playable HLS links for anything you build |

---

## Prerequisites

- **Python 3.9+**
- **VideoDB API key** -- sign up free at [console.videodb.io](https://console.videodb.io) (50 free uploads, no credit card)

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/video-db/agent-toolkit.git
cd agent-toolkit/claude/skills/videodb-python
```

### 2. Add your API key

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder with your key:

```ini
VIDEO_DB_API_KEY=your-api-key-here
```

### 3. Set up the Python environment

```bash
python scripts/setup_venv.py
```

This creates a `.venv/` directory and installs all dependencies. You only need to do this once.

### 4. Verify the connection

```bash
.venv/bin/python scripts/check_connection.py
```

If you see a success message, you're ready to go.

---

## Using with Claude Code

Claude Code discovers skills from `.claude/skills/` directories. You need to symlink (or copy) the skill folder into one of these locations.

### Option A: Personal skill (all projects)

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)" ~/.claude/skills/videodb-python
```

> Run this from inside the `agent-toolkit/claude/skills/videodb-python` directory.

### Option B: Project skill (single project)

From your project root:

```bash
mkdir -p .claude/skills
ln -s /path/to/agent-toolkit/claude/skills/videodb-python .claude/skills/videodb-python
```

### Start using it

Open Claude Code (or restart your session) and try:

```
/videodb-python upload this YouTube video and give me a transcript
```

You can also just describe what you want -- Claude will load the skill automatically when the task involves video processing.

**More examples:**

```
/videodb-python search for "product demo" in my latest video
```
```
/videodb-python add subtitles to my video with white text on black background
```
```
/videodb-python take clips from 10s-30s and 45s-60s, add a title card, and combine them
```
```
/videodb-python generate 30 seconds of background music and overlay it on my video
```

> **Why not `--add-dir`?** The `--add-dir` flag only discovers skills inside `.claude/skills/` subdirectories (note the leading dot). This repo uses `claude/skills/` (no dot), so `--add-dir` won't find it. Use the symlink approach above.

---

## Using with Claude Web (claude.ai)

You can use VideoDB with Claude on the web by giving it the SDK reference as project context.

### Setup

1. Create a new [Claude Project](https://claude.ai)
2. In the project knowledge, add the contents of these files:
   - [`SKILL.md`](SKILL.md) -- core SDK reference and quick-start patterns
   - [`REFERENCE.md`](REFERENCE.md) -- full API reference
3. Set the project system prompt to:

```
You are a video processing assistant using the VideoDB Python SDK.
Use the provided reference documentation to write correct Python code.
Always use `from dotenv import load_dotenv; load_dotenv()` before `videodb.connect()`.
```

### Usage

Ask Claude to write Python scripts for your video tasks:

- *"Write a Python script that uploads this YouTube video and generates a transcript."*
- *"Create a script that searches for 'product launch' in a video and compiles the matching clips."*
- *"Build a timeline that combines three video clips with a title overlay and background music."*

Claude will generate standalone Python scripts you can run locally with:

```bash
.venv/bin/python your_script.py
```

---

## Using with the Claude API

Use the VideoDB skill as a system prompt for programmatic access via the [Anthropic SDK](https://docs.anthropic.com/en/api/getting-started).

### Setup

1. Read `SKILL.md` and `REFERENCE.md` into your system prompt
2. Send user messages describing video tasks
3. Execute the generated Python code in your environment

### Example

```python
import anthropic

# Load the skill reference as system context
with open("SKILL.md") as f:
    skill_context = f.read()
with open("REFERENCE.md") as f:
    reference_context = f.read()

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    system=f"""You are a video processing assistant using the VideoDB Python SDK.
Write correct, runnable Python code based on user requests.

{skill_context}

{reference_context}""",
    messages=[
        {
            "role": "user",
            "content": "Upload this YouTube video and search for mentions of 'AI': https://www.youtube.com/watch?v=VIDEO_ID"
        }
    ],
)

print(message.content[0].text)
```

### Tips

- Include `SEARCH.md` or `EDITOR.md` in the system prompt when your use case focuses on search or editing
- For token efficiency, use only `SKILL.md` for general tasks -- it covers the most common operations
- Add `GENERATIVE.md` when you need AI-generated media (images, music, voice)

---

## Project Structure

```
videodb-python/
├── SKILL.md              # Skill definition (loaded by Claude Code)
├── REFERENCE.md          # Complete API reference
├── SEARCH.md             # Search and indexing guide
├── EDITOR.md             # Timeline editing guide
├── GENERATIVE.md         # AI generation guide
├── MEETINGS.md           # Meeting recording and analysis
├── RTSTREAM.md           # Real-time streaming guide
├── USE_CASES.md          # End-to-end workflow examples
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variable template
└── scripts/
    ├── setup_venv.py         # Virtual environment setup
    ├── setup.py              # Dependency checker
    ├── check_connection.py   # API key verification
    ├── batch_upload.py       # Bulk upload from URL list or directory
    ├── search_and_compile.py # Search + compile into stream
    ├── extract_clips.py      # Extract clips by timestamp
    ├── test_editor.py        # Integration test: timeline editing
    ├── test_meetings.py      # Integration test: meeting analysis
    └── test_rtstream.py      # Integration test: streaming
```

---

## Documentation

| Guide | What's Inside |
|---|---|
| [SKILL.md](SKILL.md) | Skill definition and quick reference |
| [REFERENCE.md](REFERENCE.md) | Complete API reference for all objects and methods |
| [SEARCH.md](SEARCH.md) | Semantic, keyword, and scene-based search |
| [EDITOR.md](EDITOR.md) | Timeline editing with overlays, limitations |
| [GENERATIVE.md](GENERATIVE.md) | AI-generated images, video, music, voice, and text |
| [MEETINGS.md](MEETINGS.md) | Meeting recording, transcription, and analysis |
| [RTSTREAM.md](RTSTREAM.md) | Real-time HLS streaming |
| [USE_CASES.md](USE_CASES.md) | End-to-end workflow examples |

---

## Utility Scripts

Run these directly for common tasks:

```bash
# Upload multiple files from a URL list
.venv/bin/python scripts/batch_upload.py --urls urls.txt --collection "My Project"

# Search inside a video and compile results
.venv/bin/python scripts/search_and_compile.py --video-id VIDEO_ID --query "product demo"

# Extract clips by timestamp ranges
.venv/bin/python scripts/extract_clips.py --video-id VIDEO_ID --timestamps "10.0-25.0,45.0-60.0"
```

---

## License

This skill is provided as-is for use with Claude. The VideoDB SDK is governed by its own [license](https://github.com/video-db/videodb-python/blob/main/LICENSE).
