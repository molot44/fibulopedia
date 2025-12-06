"""
Quick test script to verify pages load without errors.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

# Mock Streamlit before importing pages
sys.modules['streamlit'] = MagicMock()

def test_import_pages():
    """Test that all key pages can be imported without errors."""
    print("\n=== Testing Page Imports ===")
    
    try:
        # Mock streamlit config functions
        import streamlit as st
        st.set_page_config = MagicMock()
        st.markdown = MagicMock()
        st.sidebar = MagicMock()
        
        # Import pages - this will trigger the module-level code
        print("✓ Importing Weapons page...")
        import pages.Weapons as weapons_page
        
        print("✓ Importing Equipment page...")
        import pages.Equipment as equipment_page
        
        print("✓ All pages imported successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error importing pages: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_services():
    """Test that all services work correctly."""
    print("\n=== Testing Services ===")
    
    try:
        from src.services.weapons_service import load_weapons
        from src.services.equipment_service import load_equipment
        
        print("✓ Loading weapons...")
        weapons = load_weapons()
        print(f"  Loaded {len(weapons)} weapons")
        
        print("✓ Loading equipment...")
        equipment = load_equipment()
        print(f"  Loaded {len(equipment)} equipment items")
        
        # Check for NPCPrice objects
        weapons_with_sell_to = [w for w in weapons if w.sell_to]
        equipment_with_sell_to = [e for e in equipment if e.sell_to]
        
        print(f"  {len(weapons_with_sell_to)} weapons have sell_to data")
        print(f"  {len(equipment_with_sell_to)} equipment items have sell_to data")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing services: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all quick tests."""
    print("=" * 60)
    print("QUICK VALIDATION TEST")
    print("=" * 60)
    
    results = []
    results.append(("Services", test_services()))
    results.append(("Page Imports", test_import_pages()))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit(main())
