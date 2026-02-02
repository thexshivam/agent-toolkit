#!/usr/bin/env python3
"""
VideoDB Transcript Script

Get transcriptions from VideoDB videos.

Usage:
    python transcript.py '{"url": "https://youtu.be/xxx"}'
    python transcript.py '{"video_id": "vid_123"}'
    python transcript.py '{"video_id": "vid_123", "format": "text"}'

Environment:
    VIDEODB_API_KEY: Your VideoDB API key (required)
"""

import os
import sys
import json
import re
from pathlib import Path

# Load .env from multiple possible locations
def load_env_files():
    """Load .env files from multiple possible locations."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return

    script_dir = Path(__file__).parent.resolve()
    skill_dir = script_dir.parent
    skills_dir = skill_dir.parent

    for env_path in [
        skills_dir / '.env',
        skill_dir / '.env',
        Path.cwd() / '.env',
    ]:
        if env_path.exists():
            load_dotenv(env_path)

load_env_files()


def extract_youtube_id(url: str) -> str:
    """Extract YouTube video ID from URL."""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([\w-]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_transcript(
    video_id: str = None,
    url: str = None,
    format: str = "timestamped",
    force: bool = False
) -> dict:
    """
    Get transcript from a VideoDB video.

    Args:
        video_id: The video ID (required if no url)
        url: YouTube/video URL (will upload if not in collection)
        format: "timestamped", "text", or "both"
        force: Force regeneration of transcript

    Returns:
        dict with transcript data
    """
    # Check dependencies
    try:
        from videodb import connect
    except ImportError:
        return {
            "success": False,
            "error": "MISSING_DEPENDENCY",
            "message": "Install videodb: pip install videodb"
        }
    
    # Check API key
    api_key = os.environ.get("VIDEODB_API_KEY")
    if not api_key:
        return {
            "success": False,
            "error": "MISSING_API_KEY",
            "message": "Set VIDEODB_API_KEY environment variable"
        }
    
    # Validate format
    valid_formats = ["timestamped", "text", "both"]
    if format not in valid_formats:
        return {
            "success": False,
            "error": "INVALID_FORMAT",
            "message": f"Format must be one of: {valid_formats}"
        }

    if not video_id and not url:
        return {
            "success": False,
            "error": "MISSING_VIDEO_ID",
            "message": "video_id or url is required"
        }

    try:
        conn = connect(api_key=api_key)
        collection = conn.get_collection()

        # Helper to find or upload video from URL
        def get_video_from_url(video_url: str):
            """Find existing video or upload from URL."""
            yt_id = extract_youtube_id(video_url)
            for v in collection.get_videos():
                v_str = str(getattr(v, 'name', '')) + str(getattr(v, 'source', ''))
                if yt_id and yt_id in v_str:
                    return v
            return collection.upload(url=video_url)

        # Get video by URL or ID
        if url:
            video = get_video_from_url(url)
            video_id = video.id
        else:
            video = collection.get_video(video_id)

        if not video:
            return {
                "success": False,
                "error": "VIDEO_NOT_FOUND",
                "message": f"Video '{video_id}' not found"
            }
        
        # Get transcript data
        result = {
            "success": True,
            "video_id": video_id,
            "video_name": getattr(video, 'name', video_id),
            "duration": getattr(video, 'length', None) or getattr(video, 'duration', None)
        }

        # Try to get transcript, generate if it doesn't exist
        def ensure_transcript():
            try:
                return video.get_transcript(force=force)
            except Exception as e:
                if "does not exist" in str(e).lower() or "generate transcript" in str(e).lower():
                    video.generate_transcript()
                    return video.get_transcript()
                raise

        if format in ["timestamped", "both"]:
            transcript = ensure_transcript()
            result["transcript"] = transcript
            result["segment_count"] = len(transcript) if transcript else 0

        if format in ["text", "both"]:
            # Ensure transcript exists before getting text
            if format == "text":
                ensure_transcript()
            text = video.get_transcript_text()
            result["text"] = text
            result["word_count"] = len(text.split()) if text else 0

        return result
        
    except Exception as e:
        error_msg = str(e).lower()
        
        if "no transcript" in error_msg or "not found" in error_msg:
            return {
                "success": False,
                "error": "NO_TRANSCRIPT",
                "message": "No transcript available. Video may still be processing."
            }
        
        if "processing" in error_msg:
            return {
                "success": False,
                "error": "PROCESSING",
                "message": "Transcript is being generated. Try again in a few minutes."
            }
        
        return {
            "success": False,
            "error": "TRANSCRIPT_ERROR",
            "message": str(e)
        }


def main():
    """CLI entry point."""
    # Parse input
    if len(sys.argv) > 1:
        try:
            args = json.loads(sys.argv[1])
        except json.JSONDecodeError as e:
            print(json.dumps({"success": False, "error": "INVALID_JSON", "message": str(e)}, indent=2))
            sys.exit(1)
    else:
        try:
            args = json.load(sys.stdin)
        except Exception:
            print(json.dumps({
                "success": False,
                "error": "NO_INPUT",
                "message": "Provide JSON as argument or stdin",
                "example": '{"url": "https://youtu.be/xxx"}'
            }, indent=2))
            sys.exit(1)
    
    # Validate required field
    if "video_id" not in args and "url" not in args:
        print(json.dumps({"success": False, "error": "MISSING_VIDEO_ID", "message": "video_id or url is required"}, indent=2))
        sys.exit(1)
    
    # Get transcript
    result = get_transcript(**args)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()