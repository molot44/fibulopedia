"""
Script to clean JSON files: remove buy_from field and ensure sell_to exists.

This script updates weapons.json, equipment.json, and tools.json to:
1. Remove all buy_from fields
2. Ensure all items have a sell_to field (add empty array if missing)
3. Preserve all other data

Run this script from the project root directory.
"""

import json
from pathlib import Path

# File paths
PROJECT_ROOT = Path(__file__).parent
CONTENT_DIR = PROJECT_ROOT / "content"

FILES_TO_CLEAN = [
    CONTENT_DIR / "weapons.json",
    CONTENT_DIR / "equipment.json",
    CONTENT_DIR / "tools.json",
    CONTENT_DIR / "food.json"
]


def clean_json_file(file_path: Path) -> None:
    """
    Clean a single JSON file by removing buy_from and ensuring sell_to exists.
    
    Args:
        file_path: Path to the JSON file to clean.
    """
    print(f"\nProcessing: {file_path.name}")
    
    if not file_path.exists():
        print(f"  ⚠️  File not found, skipping...")
        return
    
    try:
        # Load JSON data
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print(f"  ⚠️  Expected list, got {type(data)}, skipping...")
            return
        
        # Track statistics
        buy_from_removed = 0
        sell_to_added = 0
        
        # Process each item
        for item in data:
            if not isinstance(item, dict):
                continue
            
            # Remove buy_from if it exists
            if "buy_from" in item:
                del item["buy_from"]
                buy_from_removed += 1
            
            # Add sell_to if it doesn't exist
            if "sell_to" not in item:
                item["sell_to"] = []
                sell_to_added += 1
        
        # Save cleaned data
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"  ✓ Processed {len(data)} items")
        print(f"  ✓ Removed buy_from from {buy_from_removed} items")
        print(f"  ✓ Added sell_to to {sell_to_added} items")
        
    except json.JSONDecodeError as e:
        print(f"  ✗ JSON decode error: {e}")
    except Exception as e:
        print(f"  ✗ Error: {e}")


def main():
    """Main function to clean all JSON files."""
    print("=" * 60)
    print("JSON CLEANUP SCRIPT")
    print("=" * 60)
    print("\nThis script will:")
    print("  1. Remove all 'buy_from' fields")
    print("  2. Ensure all items have 'sell_to' field (empty array if missing)")
    print()
    
    for file_path in FILES_TO_CLEAN:
        clean_json_file(file_path)
    
    print("\n" + "=" * 60)
    print("CLEANUP COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main()
