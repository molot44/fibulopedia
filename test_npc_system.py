"""
Test script for NPC Selling System.

Tests:
1. Loading data with NPCPrice objects
2. Validation of NPC names and locations
3. Search functionality with NPC data
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.services.weapons_service import load_weapons, search_weapons
from src.services.equipment_service import load_equipment, search_equipment
from src.services.data_loader import validate_npc_consistency, VALID_NPC_NAMES, VALID_LOCATIONS
from src.models import NPCPrice


def test_weapons_loading():
    """Test loading weapons with NPCPrice objects."""
    print("\n=== TEST 1: Loading Weapons ===")
    try:
        weapons = load_weapons()
        print(f"✓ Loaded {len(weapons)} weapons")
        
        # Check NPCPrice objects
        weapons_with_npcs = [w for w in weapons if w.sell_to]
        print(f"✓ {len(weapons_with_npcs)} weapons have sell_to data")
        
        if weapons_with_npcs:
            weapon = weapons_with_npcs[0]
            print(f"\nExample weapon: {weapon.name}")
            for npc in weapon.sell_to:
                assert isinstance(npc, NPCPrice), f"sell_to must contain NPCPrice objects, got {type(npc)}"
                print(f"  - {npc.npc} ({npc.location}): {npc.price} gp")
            print("✓ All sell_to entries are NPCPrice objects")
        
        return True
    except Exception as e:
        print(f"✗ Error loading weapons: {e}")
        return False


def test_equipment_loading():
    """Test loading equipment with NPCPrice objects."""
    print("\n=== TEST 2: Loading Equipment ===")
    try:
        equipment = load_equipment()
        print(f"✓ Loaded {len(equipment)} equipment items")
        
        # Check NPCPrice objects
        equipment_with_npcs = [e for e in equipment if e.sell_to]
        print(f"✓ {len(equipment_with_npcs)} equipment items have sell_to data")
        
        if equipment_with_npcs:
            item = equipment_with_npcs[0]
            print(f"\nExample equipment: {item.name}")
            for npc in item.sell_to:
                assert isinstance(npc, NPCPrice), f"sell_to must contain NPCPrice objects, got {type(npc)}"
                print(f"  - {npc.npc} ({npc.location}): {npc.price} gp")
            print("✓ All sell_to entries are NPCPrice objects")
        
        return True
    except Exception as e:
        print(f"✗ Error loading equipment: {e}")
        return False


def test_npc_validation():
    """Test NPC name and location validation."""
    print("\n=== TEST 3: NPC Validation ===")
    try:
        print(f"✓ Found {len(VALID_NPC_NAMES)} valid NPC names")
        print(f"✓ Found {len(VALID_LOCATIONS)} valid locations")
        
        # Test validation function
        weapons = load_weapons()
        equipment = load_equipment()
        all_items = weapons + equipment
        
        issues = validate_npc_consistency(all_items)
        
        if issues:
            print(f"\n⚠ Found {len(issues)} validation issues:")
            for issue in issues[:5]:  # Show first 5
                print(f"  - {issue}")
            if len(issues) > 5:
                print(f"  ... and {len(issues) - 5} more")
            return False
        else:
            print("✓ No validation issues found - all NPCs are consistent")
            return True
            
    except Exception as e:
        print(f"✗ Error during validation: {e}")
        return False


def test_search_functionality():
    """Test search with NPC data."""
    print("\n=== TEST 4: Search Functionality ===")
    try:
        # Search for weapons by NPC name
        results = search_weapons("rashid")
        if results:
            print(f"✓ Search for 'rashid' found {len(results)} weapons")
            print(f"  Example: {results[0].name}")
        else:
            print("✓ Search for 'rashid' returned empty (no weapons sold to Rashid)")
        
        # Search for equipment by location
        results = search_equipment("thais")
        if results:
            print(f"✓ Search for 'thais' found {len(results)} equipment items")
            print(f"  Example: {results[0].name}")
        else:
            print("✓ Search for 'thais' returned empty")
        
        return True
    except Exception as e:
        print(f"✗ Error during search: {e}")
        return False


def test_no_buy_from():
    """Test that buy_from has been removed."""
    print("\n=== TEST 5: Verify buy_from Removal ===")
    try:
        weapons = load_weapons()
        equipment = load_equipment()
        
        # Check weapons
        for weapon in weapons:
            assert not hasattr(weapon, 'buy_from'), f"Weapon {weapon.name} still has buy_from"
        print(f"✓ No weapons have buy_from field")
        
        # Check equipment
        for item in equipment:
            assert not hasattr(item, 'buy_from'), f"Equipment {item.name} still has buy_from"
        print(f"✓ No equipment items have buy_from field")
        
        return True
    except Exception as e:
        print(f"✗ Error checking buy_from: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("NPC SELLING SYSTEM - TEST SUITE")
    print("=" * 60)
    
    results = []
    results.append(("Weapons Loading", test_weapons_loading()))
    results.append(("Equipment Loading", test_equipment_loading()))
    results.append(("NPC Validation", test_npc_validation()))
    results.append(("Search Functionality", test_search_functionality()))
    results.append(("buy_from Removal", test_no_buy_from()))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit(main())
