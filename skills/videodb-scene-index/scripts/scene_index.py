#!/usr/bin/env python3
"""
VideoDB Scene Index Script

Create and search visual scene indexes.

Usage:
    # Search scenes by URL
    python scene_index.py '{"url": "https://youtu.be/xxx", "action": "search", "query": "red car"}'

    # Create scene index
    python scene_index.py '{"video_id": "vid_123", "action": "create", "prompt": "Describe objects"}'

    # Search scenes by video ID
    python scene_index.py '{"video_id": "vid_123", "action": "search", "query": "red car"}'

    # List indexes
    python scene_index.py '{"video_id": "vid_123", "action": "list"}'

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


def scene_index(
    video_id: str = None,
    url: str = None,
    action: str = "search",
    query: str = None,
    prompt: str = "Describe the visual content including people, objects, and actions.",
    extraction_type: str = "time_based",
    time_interval: int = 5,
    frame_count: int = 3,
    index_id: str = None
) -> dict:
    """
    Create or search scene indexes.

    Args:
        video_id: The video ID (required if no url)
        url: YouTube/video URL (will upload if not in collection)
        action: "create", "search", or "list"
        query: Search query (for search action)
        prompt: Vision model prompt (for create action)
        extraction_type: "time_based" or "shot_based"
        time_interval: Seconds per scene (time_based)
        frame_count: Frames to extract per scene
        index_id: Specific index ID (for search)

    Returns:
        dict with results
    """
    # Check dependencies
    try:
        from videodb import connect, IndexType, SceneExtractionType
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
    
    # Validate action
    valid_actions = ["create", "search", "list"]
    if action not in valid_actions:
        return {
            "success": False,
            "error": "INVALID_ACTION",
            "message": f"Action must be one of: {valid_actions}"
        }
    
    if action == "search" and not query:
        return {
            "success": False,
            "error": "MISSING_QUERY",
            "message": "query is required for search action"
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
        
        # Handle actions
        if action == "create":
            # Map extraction type
            ext_type = (SceneExtractionType.time_based 
                       if extraction_type == "time_based" 
                       else SceneExtractionType.shot_based)
            
            # Build config
            if extraction_type == "time_based":
                config = {"time": time_interval, "frame_count": frame_count}
            else:
                config = {"threshold": 20, "frame_count": frame_count}
            
            # Create index
            video.index_scenes(
                extraction_type=ext_type,
                extraction_config=config,
                prompt=prompt
            )
            
            return {
                "success": True,
                "action": "create",
                "video_id": video_id,
                "message": "Scene index created successfully",
                "config": {
                    "extraction_type": extraction_type,
                    "time_interval": time_interval if extraction_type == "time_based" else None,
                    "frame_count": frame_count,
                    "prompt": prompt
                }
            }
        
        elif action == "list":
            # List scene indexes
            try:
                indexes = video.list_scene_index()
                return {
                    "success": True,
                    "action": "list",
                    "video_id": video_id,
                    "indexes": [
                        {
                            "id": getattr(idx, 'id', str(idx)),
                            "created": getattr(idx, 'created_at', None)
                        }
                        for idx in (indexes or [])
                    ]
                }
            except AttributeError:
                return {
                    "success": True,
                    "action": "list",
                    "video_id": video_id,
                    "message": "List operation may not be available. Try searching directly."
                }
        
        else:  # search
            # Helper to check if scene index exists and is ready
            def get_ready_index():
                try:
                    indexes = video.list_scene_index()
                    for idx in (indexes or []):
                        idx_dict = idx if isinstance(idx, dict) else vars(idx) if hasattr(idx, '__dict__') else {}
                        status = idx_dict.get('status', str(idx))
                        if 'done' in str(status).lower() or 'ready' in str(status).lower():
                            return True
                    return False
                except:
                    return False

            # Helper to create index and wait for it
            def ensure_scene_index():
                import time
                # Check if already indexed
                if get_ready_index():
                    return True

                # Create index
                ext_type = SceneExtractionType.time_based
                config = {"time": time_interval, "frame_count": frame_count}
                video.index_scenes(
                    extraction_type=ext_type,
                    extraction_config=config,
                    prompt=prompt
                )

                # Wait for index to be ready (max 5 minutes)
                for _ in range(30):
                    time.sleep(10)
                    if get_ready_index():
                        return True
                return False

            # Try search, auto-index if needed
            try:
                results = video.search(
                    query=query,
                    index_type=IndexType.scene
                )
                if not results.get_shots():
                    raise Exception("No results - may need indexing")
            except Exception as e:
                error_msg = str(e).lower()
                if "not indexed" in error_msg or "no scene" in error_msg or "no results" in error_msg:
                    # Auto-create scene index and retry
                    if ensure_scene_index():
                        results = video.search(
                            query=query,
                            index_type=IndexType.scene
                        )
                    else:
                        return {
                            "success": False,
                            "error": "INDEXING_TIMEOUT",
                            "message": "Scene indexing is taking longer than expected. Try again later."
                        }
                else:
                    raise

            shots = results.get_shots()
            formatted = []
            for shot in shots:
                # Try multiple attribute names for score
                score = None
                for attr in ['search_score', 'score', 'relevance_score', 'confidence']:
                    score = getattr(shot, attr, None)
                    if score is not None:
                        break

                formatted.append({
                    "start": round(shot.start, 1),
                    "end": round(shot.end, 1),
                    "description": getattr(shot, 'text', ''),
                    "score": round(score, 3) if score is not None else None,
                    "stream_url": getattr(shot, 'stream_url', None)
                })

            compiled_url = results.compile() if shots else None

            return {
                "success": True,
                "action": "search",
                "video_id": video_id,
                "query": query,
                "results": formatted,
                "total_results": len(formatted),
                "compiled_stream_url": compiled_url
            }
        
    except Exception as e:
        error_msg = str(e).lower()
        
        if "not indexed" in error_msg or "no scene" in error_msg:
            return {
                "success": False,
                "error": "NOT_INDEXED",
                "message": "No scene index found. Create one first with action='create'."
            }
        
        if "processing" in error_msg:
            return {
                "success": False,
                "error": "PROCESSING",
                "message": "Scene index is being created. Try again in a few minutes."
            }
        
        return {
            "success": False,
            "error": "SCENE_INDEX_ERROR",
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
                "examples": {
                    "search": '{"url": "https://youtu.be/xxx", "action": "search", "query": "car"}',
                    "create": '{"url": "https://youtu.be/xxx", "action": "create", "prompt": "Describe objects"}',
                    "list": '{"video_id": "vid_123", "action": "list"}'
                }
            }, indent=2))
            sys.exit(1)
    
    # Validate required field
    if "video_id" not in args and "url" not in args:
        print(json.dumps({"success": False, "error": "MISSING_VIDEO_ID", "message": "video_id or url is required"}, indent=2))
        sys.exit(1)
    
    # Run
    result = scene_index(**args)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()