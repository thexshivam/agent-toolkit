#!/usr/bin/env python3
"""
VideoDB Upload Utility

Upload videos and list existing videos in your collection.

Usage:
    # Upload from URL
    python upload.py '{"url": "https://youtube.com/watch?v=..."}'

    # Upload from file
    python upload.py '{"file": "/path/to/video.mp4"}'

    # List videos
    python upload.py '{"action": "list"}'

    # Get video info
    python upload.py '{"action": "info", "video_id": "vid_123"}'

Environment:
    VIDEODB_API_KEY: Your VideoDB API key (required)
"""

import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()


def upload_video(
    url: str = None,
    file: str = None,
    action: str = "upload",
    video_id: str = None,
    name: str = None
) -> dict:
    """
    Upload videos or manage VideoDB collection.

    Args:
        url: URL to upload (YouTube, direct video link)
        file: Local file path to upload
        action: "upload", "list", or "info"
        video_id: Video ID (for info action)
        name: Optional name for uploaded video

    Returns:
        dict with results
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

    try:
        conn = connect(api_key=api_key)
        collection = conn.get_collection()

        if action == "list":
            videos = collection.get_videos()
            return {
                "success": True,
                "action": "list",
                "videos": [
                    {
                        "id": v.id,
                        "name": getattr(v, 'name', 'Unnamed'),
                        "duration": getattr(v, 'length', None) or getattr(v, 'duration', None)
                    }
                    for v in videos
                ],
                "total": len(videos)
            }

        elif action == "info":
            if not video_id:
                return {
                    "success": False,
                    "error": "MISSING_VIDEO_ID",
                    "message": "video_id required for info action"
                }

            video = collection.get_video(video_id)
            if not video:
                return {
                    "success": False,
                    "error": "VIDEO_NOT_FOUND",
                    "message": f"Video '{video_id}' not found"
                }

            return {
                "success": True,
                "action": "info",
                "video": {
                    "id": video.id,
                    "name": getattr(video, 'name', 'Unnamed'),
                    "duration": getattr(video, 'length', None) or getattr(video, 'duration', None),
                    "stream_url": getattr(video, 'stream_url', None)
                }
            }

        else:  # upload
            if not url and not file:
                return {
                    "success": False,
                    "error": "MISSING_SOURCE",
                    "message": "Provide 'url' or 'file' to upload"
                }

            if url:
                video = collection.upload(url=url, name=name)
            else:
                if not os.path.exists(file):
                    return {
                        "success": False,
                        "error": "FILE_NOT_FOUND",
                        "message": f"File not found: {file}"
                    }
                video = collection.upload(file_path=file, name=name)

            return {
                "success": True,
                "action": "upload",
                "video": {
                    "id": video.id,
                    "name": getattr(video, 'name', 'Unnamed'),
                    "duration": getattr(video, 'length', None) or getattr(video, 'duration', None)
                },
                "message": "Video uploaded successfully. Use this video_id to test other skills."
            }

    except Exception as e:
        return {
            "success": False,
            "error": "UPLOAD_ERROR",
            "message": str(e)
        }


def main():
    """CLI entry point."""
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
                "examples": {
                    "upload_url": '{"url": "https://youtube.com/shorts/0TKl2skt4sk?si=Ya7YMyi-emREf0LA"}',
                    "upload_file": '{"file": "/path/to/video.mp4"}',
                    "list": '{"action": "list"}',
                    "info": '{"action": "info", "video_id": "vid_123"}'
                }
            }, indent=2))
            sys.exit(1)

    result = upload_video(**args)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
