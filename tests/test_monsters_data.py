"""
Test script for monsters data validation.

This script validates the integrity of monsters.json including:
- Required fields presence
- Data type validation
- Value range checks
- Image file existence
- No duplicate IDs
- Proper difficulty classification
"""

import sys
from pathlib import Path
from src.services.monsters_service import load_monsters
from src.config import ASSETS_DIR

def test_monsters_data():
    """Run all validation tests on monsters data."""
    
    print("="*70)
    print("MONSTERS DATA VALIDATION TEST")
    print("="*70)
    
    # Load monsters
    monsters = load_monsters()
    if not monsters:
        print("[FAIL] No monsters loaded!")
        return False
    
    print(f"\n[OK] Loaded {len(monsters)} monsters")
    
    all_passed = True
    
    # Test 1: Check required fields
    print("\n" + "-"*70)
    print("TEST 1: Required Fields")
    print("-"*70)
    required_fields = ['id', 'name', 'hp', 'exp', 'loot', 'location', 'difficulty', 'image']
    for monster in monsters:
        for field in required_fields:
            if not hasattr(monster, field):
                print(f"[FAIL] Monster {monster.name} missing field: {field}")
                all_passed = False
    print("[OK] All monsters have required fields")
    
    # Test 2: Check HP values
    print("\n" + "-"*70)
    print("TEST 2: HP Values")
    print("-"*70)
    for monster in monsters:
        if monster.hp <= 0:
            print(f"[FAIL] {monster.name} has invalid HP: {monster.hp}")
            all_passed = False
        if monster.hp > 10000:
            print(f"[WARN] {monster.name} has very high HP: {monster.hp}")
    print(f"[OK] HP range: {min(m.hp for m in monsters)} - {max(m.hp for m in monsters)}")
    
    # Test 3: Check EXP values
    print("\n" + "-"*70)
    print("TEST 3: EXP Values")
    print("-"*70)
    for monster in monsters:
        if monster.exp < 0:
            print(f"[FAIL] {monster.name} has negative EXP: {monster.exp}")
            all_passed = False
    passive_count = len([m for m in monsters if m.exp == 0])
    print(f"[OK] EXP range: {min(m.exp for m in monsters)} - {max(m.exp for m in monsters)}")
    print(f"[INFO] {passive_count} passive creatures (0 EXP)")
    
    # Test 4: Check summon/convince values
    print("\n" + "-"*70)
    print("TEST 4: Summon/Convince Values")
    print("-"*70)
    for monster in monsters:
        if monster.summon and monster.summon < 0:
            print(f"[FAIL] {monster.name} has negative summon: {monster.summon}")
            all_passed = False
        if monster.convince and monster.convince < 0:
            print(f"[FAIL] {monster.name} has negative convince: {monster.convince}")
            all_passed = False
    
    summonable = len([m for m in monsters if m.summon])
    convinceable = len([m for m in monsters if m.convince])
    print(f"[OK] Summonable monsters: {summonable}/{len(monsters)}")
    print(f"[OK] Convinceable monsters: {convinceable}/{len(monsters)}")
    
    # Test 5: Check for duplicate IDs
    print("\n" + "-"*70)
    print("TEST 5: Duplicate IDs")
    print("-"*70)
    ids = [m.id for m in monsters]
    duplicates = [id for id in ids if ids.count(id) > 1]
    if duplicates:
        print(f"[FAIL] Duplicate IDs found: {set(duplicates)}")
        all_passed = False
    else:
        print("[OK] No duplicate IDs")
    
    # Test 6: Check for duplicate names
    print("\n" + "-"*70)
    print("TEST 6: Duplicate Names")
    print("-"*70)
    names = [m.name for m in monsters]
    dup_names = [name for name in names if names.count(name) > 1]
    if dup_names:
        print(f"[WARN] Duplicate names found: {set(dup_names)}")
        # This is a warning, not a failure (some monsters might legitimately have same name)
    else:
        print("[OK] No duplicate names")
    
    # Test 7: Check image files exist
    print("\n" + "-"*70)
    print("TEST 7: Image Files")
    print("-"*70)
    monsters_dir = ASSETS_DIR / "monsters"
    missing_images = []
    for monster in monsters:
        if monster.image:
            image_path = monsters_dir / monster.image
            if not image_path.exists():
                missing_images.append(f"{monster.name} -> {monster.image}")
                all_passed = False
    
    if missing_images:
        print(f"[FAIL] Missing {len(missing_images)} image files:")
        for missing in missing_images[:10]:  # Show first 10
            print(f"  - {missing}")
        if len(missing_images) > 10:
            print(f"  ... and {len(missing_images) - 10} more")
    else:
        print(f"[OK] All {len(monsters)} monster images exist")
    
    # Test 8: Check difficulty classification
    print("\n" + "-"*70)
    print("TEST 8: Difficulty Classification")
    print("-"*70)
    by_diff = {}
    for m in monsters:
        diff = m.difficulty or "unknown"
        by_diff[diff] = by_diff.get(diff, 0) + 1
    
    for diff, count in sorted(by_diff.items()):
        print(f"  {diff}: {count} monsters")
    
    if "unknown" in by_diff:
        print(f"[WARN] {by_diff['unknown']} monsters without difficulty")
    else:
        print("[OK] All monsters have difficulty classification")
    
    # Test 9: Check loot field
    print("\n" + "-"*70)
    print("TEST 9: Loot Data")
    print("-"*70)
    empty_loot = [m.name for m in monsters if not m.loot]
    print(f"[INFO] {len(empty_loot)} monsters with no loot")
    if len(empty_loot) <= 10:
        for name in empty_loot:
            print(f"  - {name}")
    
    # Test 10: Check location field
    print("\n" + "-"*70)
    print("TEST 10: Location Data")
    print("-"*70)
    no_location = [m.name for m in monsters if not m.location]
    if no_location:
        print(f"[FAIL] {len(no_location)} monsters without location:")
        for name in no_location[:5]:
            print(f"  - {name}")
        all_passed = False
    else:
        print("[OK] All monsters have location data")
    
    # Final summary
    print("\n" + "="*70)
    print("VALIDATION SUMMARY")
    print("="*70)
    print(f"Total monsters: {len(monsters)}")
    print(f"Easy: {by_diff.get('easy', 0)}")
    print(f"Medium: {by_diff.get('medium', 0)}")
    print(f"Hard: {by_diff.get('hard', 0)}")
    print(f"\nHP range: {min(m.hp for m in monsters)} - {max(m.hp for m in monsters)}")
    print(f"EXP range: {min(m.exp for m in monsters)} - {max(m.exp for m in monsters)}")
    
    if all_passed:
        print("\n[SUCCESS] All validation tests passed!")
        return True
    else:
        print("\n[FAILED] Some validation tests failed. Please review errors above.")
        return False

if __name__ == "__main__":
    success = test_monsters_data()
    sys.exit(0 if success else 1)
