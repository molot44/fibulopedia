"""Test script to generate sample analytics data for testing charts."""
from src.analytics_utils import track_page_view
import uuid
from datetime import datetime, timedelta
import random

print("Generating sample analytics data...")

# Simulate different hours throughout the day
pages = ['Home', 'Weapons', 'Equipment', 'Monsters', 'Quests', 'Loot Calculator']

# Generate data for the past 7 days
for day in range(7):
    date = datetime.now() - timedelta(days=day)
    
    # Different activity patterns for different times
    for hour in range(24):
        # More activity during peak hours (10-22)
        if 10 <= hour <= 22:
            views_count = random.randint(3, 10)
        else:
            views_count = random.randint(0, 3)
        
        for _ in range(views_count):
            # Create unique session for each view
            sid = str(uuid.uuid4())
            
            # Pick random page (Home is more popular)
            page = random.choices(
                pages,
                weights=[30, 20, 15, 20, 10, 5],
                k=1
            )[0]
            
            # Track page view
            track_page_view(page, sid)

print("\n✅ Sample data generated successfully!")
print("\nYou can now view the charts in Admin Analytics page.")
print("The charts will show:")
print("- Activity by hour (24-hour format)")
print("- Activity by day of week")
print("- Activity over time (last 7 days)")
