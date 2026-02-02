# VideoDB Skills for Claude Code

Search, analyze, and transcribe videos using natural language with [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and [VideoDB](https://videodb.io).

## Available Skills

| Skill | Description | Example Prompt |
|-------|-------------|----------------|
| **videodb-search** | Search videos by spoken content | "find where they talk about pricing" |
| **videodb-scene-index** | Search videos by visual content | "find scenes with a red car" |
| **videodb-transcript** | Get video transcriptions | "get the transcript of this video" |

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/video-db/agent-toolkit.git
cd agent-toolkit/skills
```

### 2. Get your VideoDB API key

Sign up at [console.videodb.io](https://console.videodb.io) to get your free API key (50 free uploads).

### 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and add your API key:
```
VIDEODB_API_KEY=your-api-key-here
```

### 4. Run setup

```bash
./setup.sh
```

### 5. Install skills to Claude Code

```bash
# Create Claude skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Create symlinks for all skills
ln -s "$(pwd)/videodb-search" ~/.claude/skills/
ln -s "$(pwd)/videodb-scene-index" ~/.claude/skills/
ln -s "$(pwd)/videodb-transcript" ~/.claude/skills/
```

### 6. Restart Claude Code

```bash
claude
```

## Usage in Claude Code

Once installed, simply use natural language:

### Search by spoken content
```
search for "machine learning" in https://youtu.be/VIDEO_ID
```

### Search by visual content
```
find scenes with "person presenting" in https://youtu.be/VIDEO_ID
```

### Get transcript
```
get transcript of https://youtu.be/VIDEO_ID
```

## CLI Usage

You can also run skills directly from the command line:

```bash
# Search video by spoken content
./run.sh search '{"url": "https://youtu.be/VIDEO_ID", "query": "your search term"}'

# Search video by visual content
./run.sh scene-index '{"url": "https://youtu.be/VIDEO_ID", "action": "search", "query": "red car"}'

# Get transcript
./run.sh transcript '{"url": "https://youtu.be/VIDEO_ID"}'

# You can also use video_id if already uploaded
./run.sh search '{"video_id": "m-xxxxx", "query": "your search term"}'
```

## Folder Structure

```
skills/
├── .env.example              # Environment template
├── .env                      # Your API key (create this)
├── requirements.txt          # Python dependencies
├── setup.sh                  # One-time setup script
├── run.sh                    # Unified CLI runner
├── venv/                     # Virtual environment (created by setup)
│
├── videodb-search/           # Skill 1: Spoken Content Search
│   ├── SKILL.md
│   └── scripts/search.py
│
├── videodb-scene-index/      # Skill 2: Visual Scene Search
│   ├── SKILL.md
│   └── scripts/scene_index.py
│
└── videodb-transcript/       # Skill 3: Transcription
    ├── SKILL.md
    └── scripts/transcript.py
```

## Skill Parameters

### videodb-search

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes* | YouTube or video URL |
| `video_id` | string | Yes* | VideoDB video ID |
| `query` | string | Yes | Search query |
| `search_type` | string | No | `semantic` (default) or `keyword` |
| `result_threshold` | int | No | Max results (default: 5) |

*Either `url` or `video_id` is required

### videodb-scene-index

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes* | YouTube or video URL |
| `video_id` | string | Yes* | VideoDB video ID |
| `action` | string | Yes | `search`, `create`, or `list` |
| `query` | string | For search | Visual search query |
| `prompt` | string | For create | Custom vision prompt |

### videodb-transcript

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes* | YouTube or video URL |
| `video_id` | string | Yes* | VideoDB video ID |
| `format` | string | No | `timestamped`, `text`, or `both` |

## Troubleshooting

### "MISSING_API_KEY" error
Make sure your `.env` file exists and contains a valid `VIDEODB_API_KEY`.

### "MISSING_DEPENDENCY" error
Run `./setup.sh` to install required Python packages.

### Skills not appearing in Claude Code
1. Verify symlinks exist: `ls -la ~/.claude/skills/`
2. Restart Claude Code
3. Check that SKILL.md files exist in each skill folder

### Video upload taking long
First-time YouTube uploads may take 1-2 minutes depending on video length. Subsequent searches on the same video are instant.

## Uninstall

```bash
# Remove symlinks from Claude Code
rm ~/.claude/skills/videodb-search
rm ~/.claude/skills/videodb-scene-index
rm ~/.claude/skills/videodb-transcript
```

## How Skills Work

1. **SKILL.md** - Instructions Claude reads when the skill is triggered
2. **scripts/** - Python scripts that Claude executes
3. Claude automatically triggers skills based on the `description` in SKILL.md

## Resources

- [VideoDB Documentation](https://docs.videodb.io)
- [VideoDB Console](https://console.videodb.io)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [VideoDB Discord](https://discord.gg/py9P639jGz)

## License

MIT
