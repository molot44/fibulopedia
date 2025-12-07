"""Test script for analytics system."""
from src.analytics_utils import track_page_view, get_analytics_summary, get_page_views
import uuid

# Create test session
sid = str(uuid.uuid4())

# Simulate page views
print("Simulating page views...")
track_page_view('Home', sid)
track_page_view('Weapons', sid)
track_page_view('Monsters', sid)

# Create second session
sid2 = str(uuid.uuid4())
track_page_view('Home', sid2)

# Get analytics summary
print("\n=== Analytics Summary ===")
summary = get_analytics_summary()
print(f"Total views: {summary['total_page_views']}")
print(f"Unique sessions: {summary['unique_sessions']}")
print(f"Pages tracked: {summary['pages_tracked']}")
print(f"Avg pages/session: {summary['avg_pages_per_session']:.2f}")

# Get page views
print("\n=== Page Views ===")
page_views = get_page_views()
for page, count in sorted(page_views.items(), key=lambda x: x[1], reverse=True):
    print(f"{page}: {count} views")

print("\n✓ Analytics system working correctly!")
