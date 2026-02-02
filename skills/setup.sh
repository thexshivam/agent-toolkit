#!/bin/bash
# Unified setup script for all VideoDB skills

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

echo "Setting up VideoDB skills..."

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate and install dependencies
echo "Installing dependencies..."
source "$VENV_DIR/bin/activate"
pip install -q -r "$SCRIPT_DIR/requirements.txt"

echo ""
echo "Setup complete!"
echo ""
echo "Available skills:"
echo "  - videodb-search     : Search videos by spoken content"
echo "  - videodb-scene-index: Search videos by visual content"
echo "  - videodb-transcript : Get video transcriptions"
echo ""
echo "Usage:"
echo "  ./run.sh search      '{\"url\": \"https://youtu.be/xxx\", \"query\": \"topic\"}'"
echo "  ./run.sh scene-index '{\"url\": \"https://youtu.be/xxx\", \"action\": \"search\", \"query\": \"car\"}'"
echo "  ./run.sh transcript  '{\"url\": \"https://youtu.be/xxx\"}'"
echo ""
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo "WARNING: No .env file found. Create one with:"
    echo "  echo 'VIDEODB_API_KEY=your-api-key' > $SCRIPT_DIR/.env"
fi
