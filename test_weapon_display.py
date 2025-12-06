"""
Test specific weapon display with NPCPrice data.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.services.weapons_service import load_weapons


def test_weapon_display():
    """Test how weapon with multiple NPCs is displayed."""
    print("=" * 60)
    print("WEAPON DISPLAY TEST - Two Handed Sword")
    print("=" * 60)
    
    weapons = load_weapons()
    
    # Find Two Handed Sword
    two_handed_sword = None
    for weapon in weapons:
        if weapon.name == "Two Handed Sword":
            two_handed_sword = weapon
            break
    
    if not two_handed_sword:
        print("✗ Two Handed Sword not found")
        return
    
    print(f"\nWeapon: {two_handed_sword.name}")
    print(f"Attack: {two_handed_sword.attack}")
    print(f"Defense: {two_handed_sword.defense}")
    print(f"\nSell To ({len(two_handed_sword.sell_to)} NPCs):")
    
    # Group by price
    price_groups = {}
    for npc_price in two_handed_sword.sell_to:
        price = npc_price.price
        if price not in price_groups:
            price_groups[price] = []
        npc_info = f"{npc_price.npc}"
        if npc_price.location:
            npc_info += f" ({npc_price.location})"
        price_groups[price].append(npc_info)
    
    # Display grouped by price
    for price in sorted(price_groups.keys(), reverse=True):
        print(f"\n  {price} gp:")
        for npc_info in price_groups[price]:
            print(f"    • {npc_info}")
    
    print("\n" + "=" * 60)
    print("Tooltip HTML Preview:")
    print("=" * 60)
    
    # Simulate tooltip generation from Weapons.py
    sell_to_tooltip = ""
    for price in sorted(price_groups.keys(), reverse=True):
        sell_to_tooltip += f"Sell To ({price} gp)||"
        for npc_info in price_groups[price]:
            sell_to_tooltip += f"{npc_info}||"
    
    print(sell_to_tooltip)
    
    # Display as it would appear in the table
    print("\n" + "=" * 60)
    print("Table Cell Preview:")
    print("=" * 60)
    print(f"💰 {len(two_handed_sword.sell_to)} NPCs")
    print("(hover would show tooltip with grouped prices)")


if __name__ == "__main__":
    test_weapon_display()
