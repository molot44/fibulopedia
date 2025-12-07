"""
Analytics utilities for Fibulopedia.

Simple page view tracking system that works alongside streamlit-analytics2.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
from collections import Counter
import threading

# Thread lock for safe file writing
_lock = threading.Lock()

ANALYTICS_FILE = Path("page_analytics.json")


def track_page_view(page_name: str, session_id: str = None) -> None:
    """
    Track a page view by recording it in the analytics file.
    
    Args:
        page_name: Name of the page being viewed (e.g., "Home", "Weapons", "Monsters")
        session_id: Optional session ID for unique visitor tracking
    """
    with _lock:
        # Load existing data
        data = _load_analytics_data()
        
        # Initialize structure if needed
        if "page_views" not in data:
            data["page_views"] = {}
        if "sessions" not in data:
            data["sessions"] = {}
        if "timeline" not in data:
            data["timeline"] = []
        
        # Update page view count
        if page_name not in data["page_views"]:
            data["page_views"][page_name] = 0
        data["page_views"][page_name] += 1
        
        # Track session if provided
        if session_id:
            if session_id not in data["sessions"]:
                data["sessions"][session_id] = {
                    "first_seen": datetime.now().isoformat(),
                    "pages_visited": []
                }
            if page_name not in data["sessions"][session_id]["pages_visited"]:
                data["sessions"][session_id]["pages_visited"].append(page_name)
            data["sessions"][session_id]["last_seen"] = datetime.now().isoformat()
        
        # Add to timeline (keep last 1000 entries)
        data["timeline"].append({
            "page": page_name,
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id
        })
        data["timeline"] = data["timeline"][-1000:]  # Keep only last 1000
        
        # Save data
        _save_analytics_data(data)


def get_page_views() -> Dict[str, int]:
    """Get page view counts for all pages."""
    data = _load_analytics_data()
    return data.get("page_views", {})


def get_total_page_views() -> int:
    """Get total number of page views across all pages."""
    page_views = get_page_views()
    return sum(page_views.values())


def get_unique_sessions() -> int:
    """Get count of unique sessions."""
    data = _load_analytics_data()
    return len(data.get("sessions", {}))


def get_analytics_summary() -> Dict[str, Any]:
    """Get summary of all analytics data."""
    data = _load_analytics_data()
    page_views = data.get("page_views", {})
    sessions = data.get("sessions", {})
    
    # Calculate average pages per session
    total_pages_visited = sum(len(s.get("pages_visited", [])) for s in sessions.values())
    avg_pages_per_session = total_pages_visited / len(sessions) if sessions else 0
    
    return {
        "total_page_views": sum(page_views.values()),
        "unique_sessions": len(sessions),
        "pages_tracked": len(page_views),
        "avg_pages_per_session": round(avg_pages_per_session, 2),
        "page_views": page_views,
        "most_popular_page": max(page_views.items(), key=lambda x: x[1]) if page_views else ("N/A", 0)
    }


def get_timeline_data() -> List[Dict[str, Any]]:
    """Get timeline of all page views."""
    data = _load_analytics_data()
    return data.get("timeline", [])


def get_hourly_activity() -> Dict[int, int]:
    """Get page views grouped by hour of day (0-23)."""
    timeline = get_timeline_data()
    hourly_counts = Counter()
    
    for entry in timeline:
        try:
            timestamp = datetime.fromisoformat(entry["timestamp"])
            hour = timestamp.hour
            hourly_counts[hour] += 1
        except (ValueError, KeyError):
            continue
    
    # Return all 24 hours, even if some have 0 views
    return {hour: hourly_counts.get(hour, 0) for hour in range(24)}


def get_daily_activity() -> Dict[str, int]:
    """Get page views grouped by day of week."""
    timeline = get_timeline_data()
    daily_counts = Counter()
    
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    for entry in timeline:
        try:
            timestamp = datetime.fromisoformat(entry["timestamp"])
            day_name = day_names[timestamp.weekday()]
            daily_counts[day_name] += 1
        except (ValueError, KeyError):
            continue
    
    # Return all days in order, even if some have 0 views
    return {day: daily_counts.get(day, 0) for day in day_names}


def get_activity_by_date() -> Dict[str, int]:
    """Get page views grouped by date (YYYY-MM-DD)."""
    timeline = get_timeline_data()
    date_counts = Counter()
    
    for entry in timeline:
        try:
            timestamp = datetime.fromisoformat(entry["timestamp"])
            date_str = timestamp.strftime("%Y-%m-%d")
            date_counts[date_str] += 1
        except (ValueError, KeyError):
            continue
    
    return dict(sorted(date_counts.items()))


def reset_analytics() -> None:
    """Reset all analytics data."""
    with _lock:
        _save_analytics_data({
            "page_views": {},
            "sessions": {},
            "timeline": []
        })


def _load_analytics_data() -> Dict[str, Any]:
    """Load analytics data from file."""
    if not ANALYTICS_FILE.exists():
        return {
            "page_views": {},
            "sessions": {},
            "timeline": []
        }
    
    try:
        with open(ANALYTICS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {
            "page_views": {},
            "sessions": {},
            "timeline": []
        }


def _save_analytics_data(data: Dict[str, Any]) -> None:
    """Save analytics data to file."""
    try:
        with open(ANALYTICS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving analytics data: {e}")
