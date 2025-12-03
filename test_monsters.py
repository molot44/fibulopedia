"""Quick test script for monsters data."""
import json
from pathlib import Path

# Load and validate JSON
data = json.load(open('content/monsters.json', 'r', encoding='utf-8'))
print(f'✅ JSON valid - {len(data)} monsters loaded')
print(f'First monster: {data[0]["name"]}')
print(f'  - has image: {"image" in data[0]}')
print(f'  - has summon: {"summon" in data[0]}')
print(f'  - has loot_items: {"loot_items" in data[0]}')

if "loot_items" in data[0]:
    print(f'  - loot items count: {len(data[0]["loot_items"])}')
    for item in data[0]["loot_items"]:
        print(f'    - {item["name"]}: {item["min"]}-{item["max"]}x (image: {item["image"]})')

# Test image paths
assets_path = Path('assets/monsters')
for monster in data[:3]:
    name = monster["name"]
    if "image" in monster and monster["image"]:
        image_file = assets_path / monster["image"]
        exists = "✅" if image_file.exists() else "❌"
        print(f'{exists} {name}: {monster["image"]}')
