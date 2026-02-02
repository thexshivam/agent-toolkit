#!/usr/bin/env python3
"""
VideoDB Search Script

Search within videos or collections using natural language.

Usage:
    python search.py '{"video_id": "vid_123", "query": "pricing"}'
    python search.py '{"url": "https://youtu.be/xxx", "query": "topic"}'
    python search.py '{"query": "product demo", "scope": "collection"}'

Environment:
    VIDEODB_API_KEY: Your VideoDB API key (required)
"""

import os
import sys
import json
import re
from pathlib import Path

# Load .env from current dir, parent dirs, or skill directory
def load_env_files():
    """Load .env files from multiple possible locations."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return  # dotenv not installed, rely on environment variables

    script_dir = Path(__file__).parent.resolve()
    skill_dir = script_dir.parent
    skills_dir = skill_dir.parent

    # Try multiple locations (later ones override earlier)
    for env_path in [
        skills_dir / '.env',      # /skills/.env
        skill_dir / '.env',       # /skills/videodb-search/.env
        script_dir / '.env',      # /skills/videodb-search/scripts/.env
        Path.cwd() / '.env',      # current working directory
    ]:
        if env_path.exists():
            load_dotenv(env_path)

load_env_files()


def is_url(s: str) -> bool:
    """Check if string is a URL."""
    return s.startswith(('http://', 'https://')) if s else False


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


def search_videodb(
    query: str,
    video_id: str = None,
    url: str = None,
    scope: str = "video",
    search_type: str = "semantic",
    index_type: str = "spoken_word",
    result_threshold: int = 5,
    score_threshold: float = 0.2
) -> dict:
    """
    Search VideoDB videos or collections.

    Args:
        query: Natural language search query
        video_id: Video ID (required if scope is "video" and no url)
        url: YouTube/video URL (will upload if not in collection)
        scope: "video" or "collection"
        search_type: "semantic" or "keyword"
        index_type: "spoken_word" or "scene"
        result_threshold: Maximum number of results
        score_threshold: Minimum relevance score (0-1)

    Returns:
        dict with search results
    """
    # Check dependencies
    try:
        from videodb import connect, SearchType, IndexType
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
    
    # Validate inputs
    if scope == "video" and not video_id and not url:
        return {
            "success": False,
            "error": "MISSING_VIDEO_ID",
            "message": "video_id or url required when scope is 'video'"
        }
    
    # Map string types to enums
    search_type_map = {"semantic": SearchType.semantic, "keyword": SearchType.keyword}
    index_type_map = {"spoken_word": IndexType.spoken_word, "scene": IndexType.scene}
    
    st = search_type_map.get(search_type.lower())
    it = index_type_map.get(index_type.lower())
    
    if not st:
        return {"success": False, "error": "INVALID_SEARCH_TYPE", "message": f"Use 'semantic' or 'keyword'"}
    if not it:
        return {"success": False, "error": "INVALID_INDEX_TYPE", "message": f"Use 'spoken_word' or 'scene'"}
    
    try:
        conn = connect(api_key=api_key)
        collection = conn.get_collection()
        
        # Helper to ensure video is indexed
        def ensure_indexed(video, idx_type):
            """Index video if not already indexed."""
            try:
                if idx_type == IndexType.spoken_word:
                    video.index_spoken_words()
                else:
                    video.index_scenes()
            except Exception as e:
                # Ignore "already indexed" errors
                if "already" not in str(e).lower():
                    raise

        # Helper to find or upload video from URL
        def get_video_from_url(video_url: str):
            """Find existing video or upload from URL."""
            yt_id = extract_youtube_id(video_url)

            # Check if video already exists
            for v in collection.get_videos():
                v_str = str(getattr(v, 'name', '')) + str(getattr(v, 'source', ''))
                if yt_id and yt_id in v_str:
                    return v, False

            # Upload new video
            return collection.upload(url=video_url), True

        # Execute search based on scope
        if scope == "collection":
            results = collection.search(
                query=query,
                index_type=it,
                result_threshold=result_threshold,
                score_threshold=score_threshold
            )
        else:
            # Get video by URL or ID
            if url:
                video, is_new = get_video_from_url(url)
                video_id = video.id
                # Ensure indexing for URL-based videos
                ensure_indexed(video, it)
            else:
                video = collection.get_video(video_id)
                if not video:
                    return {"success": False, "error": "VIDEO_NOT_FOUND", "message": f"Video '{video_id}' not found"}

            # Try search, auto-index only if actually not indexed
            try:
                results = video.search(
                    query=query,
                    search_type=st,
                    index_type=it,
                    result_threshold=result_threshold,
                    score_threshold=score_threshold
                )
            except Exception as e:
                error_msg = str(e).lower()
                if "not indexed" in error_msg or "index" in error_msg:
                    # Auto-index and retry
                    ensure_indexed(video, it)
                    results = video.search(
                        query=query,
                        search_type=st,
                        index_type=it,
                        result_threshold=result_threshold,
                        score_threshold=score_threshold
                    )
                else:
                    raise
        
        # Format results
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
                "video_id": getattr(shot, 'video_id', video_id),
                "start": round(shot.start, 1),
                "end": round(shot.end, 1),
                "text": getattr(shot, 'text', ''),
                "score": round(score, 3) if score is not None else None,
                "stream_url": getattr(shot, 'stream_url', None)
            })
        
        # Compile stream
        compiled_url = results.compile() if shots else None
        
        return {
            "success": True,
            "query": query,
            "scope": scope,
            "video_id": video_id,
            "results": formatted,
            "total_results": len(formatted),
            "compiled_stream_url": compiled_url
        }
        
    except Exception as e:
        error_msg = str(e).lower()
        if "not indexed" in error_msg:
            return {
                "success": False,
                "error": "NOT_INDEXED",
                "message": "Video not indexed. Run video.index_spoken_words() first."
            }
        return {"success": False, "error": "SEARCH_ERROR", "message": str(e)}


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
                "example": '{"url": "https://youtu.be/xxx", "query": "search term"}'
            }, indent=2))
            sys.exit(1)
    
    # Validate required field
    if "query" not in args:
        print(json.dumps({"success": False, "error": "MISSING_QUERY", "message": "query is required"}, indent=2))
        sys.exit(1)
    
    # Run search
    result = search_videodb(**args)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()