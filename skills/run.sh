#!/bin/bash
# Unified runner for all VideoDB skills
# Usage: ./run.sh <skill> '<json_args>'
#   ./run.sh search '{"url": "https://youtu.be/xxx", "query": "topic"}'
#   ./run.sh scene-index '{"url": "https://youtu.be/xxx", "action": "search", "query": "car"}'
#   ./run.sh transcript '{"url": "https://youtu.be/xxx"}'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

# Show usage if no arguments
if [ $# -lt 1 ]; then
    echo "Usage: ./run.sh <skill> '<json_args>'"
    echo ""
    echo "Skills:"
    echo "  search       - Search video by spoken content"
    echo "  scene-index  - Search video by visual content"
    echo "  transcript   - Get video transcription"
    echo ""
    echo "Examples:"
    echo "  ./run.sh search '{\"url\": \"https://youtu.be/xxx\", \"query\": \"topic\"}'"
    echo "  ./run.sh scene-index '{\"url\": \"https://youtu.be/xxx\", \"action\": \"search\", \"query\": \"car\"}'"
    echo "  ./run.sh transcript '{\"url\": \"https://youtu.be/xxx\"}'"
    exit 1
fi

SKILL="$1"
shift
ARGS="$@"

# Map skill name to script path
case "$SKILL" in
    search)
        SCRIPT="$SCRIPT_DIR/videodb-search/scripts/search.py"
        ;;
    scene-index|scene)
        SCRIPT="$SCRIPT_DIR/videodb-scene-index/scripts/scene_index.py"
        ;;
    transcript)
        SCRIPT="$SCRIPT_DIR/videodb-transcript/scripts/transcript.py"
        ;;
    *)
        echo "Error: Unknown skill '$SKILL'"
        echo "Available: search, scene-index, transcript"
        exit 1
        ;;
esac

# Check if script exists
if [ ! -f "$SCRIPT" ]; then
    echo "Error: Script not found: $SCRIPT"
    exit 1
fi

# Auto-setup venv if needed
if [ ! -d "$VENV_DIR" ]; then
    echo "Setting up virtual environment..." >&2
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    pip install -q videodb python-dotenv
else
    source "$VENV_DIR/bin/activate"
fi

# Load .env
if [ -f "$SCRIPT_DIR/.env" ]; then
    export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
fi

# Run the skill
python3 "$SCRIPT" "$ARGS"
