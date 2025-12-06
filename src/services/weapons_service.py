"""
Weapons service for Fibulopedia.

This module handles loading, parsing, and querying weapon data.
It provides functions to get all weapons, filter by type, search by name,
and retrieve individual weapon details.

Version: 2.0 - Refactored to use NPCPrice dataclass and removed buy_from support.
"""

from typing import Optional

import streamlit as st

from src.config import WEAPONS_FILE
from src.models import Weapon, NPCPrice
from src.services.data_loader import (
    load_json,
    validate_required_fields,
    safe_int,
    safe_float,
    safe_list,
    parse_npc_prices
)
from src.logging_utils import setup_logger

logger = setup_logger(__name__)


def load_weapons() -> list[Weapon]:
    """
    Load all weapons from the weapons.json file.
    
    Returns:
        List of Weapon objects, or an empty list if loading fails.
    
    Example:
        >>> weapons = load_weapons()
        >>> print(f"Loaded {len(weapons)} weapons")
    """
    data = load_json(WEAPONS_FILE)
    
    if not data or not isinstance(data, list):
        logger.warning("No weapons data available or invalid format")
        return []
    
    weapons = []
    for item in data:
        if not validate_required_fields(
            item,
            ["id", "type", "name", "attack", "defense", "weight"],
            "Weapon"
        ):
            continue
        
        try:
            weapon = Weapon(
                id=str(item["id"]),
                type=str(item["type"]),
                name=str(item["name"]),
                attack=safe_int(item["attack"]),
                defense=safe_int(item["defense"]),
                weight=safe_float(item["weight"]),
                hands=str(item.get("hands", "One-handed")),
                image=item.get("image"),
                dropped_by=safe_list(item.get("dropped_by")),
                sell_to=parse_npc_prices(
                    item.get("sell_to"),
                    validate=True,
                    item_name=item.get("name", "unknown")
                ),
                reward_from=safe_list(item.get("reward_from")),
                description=item.get("description")
            )
            weapons.append(weapon)
        except Exception as e:
            logger.error(f"Error parsing weapon {item.get('id', 'unknown')}: {e}")
    
    logger.info(f"Loaded {len(weapons)} weapons")
    return weapons


def get_weapon_by_id(weapon_id: str) -> Optional[Weapon]:
    """
    Get a specific weapon by its ID.
    
    Args:
        weapon_id: The unique ID of the weapon.
    
    Returns:
        The Weapon object if found, None otherwise.
    
    Example:
        >>> weapon = get_weapon_by_id("sword_001")
        >>> if weapon:
        ...     print(weapon.name)
    """
    weapons = load_weapons()
    for weapon in weapons:
        if weapon.id == weapon_id:
            return weapon
    return None


def filter_weapons_by_type(weapon_type: str) -> list[Weapon]:
    """
    Filter weapons by their type.
    
    Args:
        weapon_type: The weapon type to filter by (sword, axe, club, distance).
    
    Returns:
        List of weapons matching the specified type.
    
    Example:
        >>> swords = filter_weapons_by_type("sword")
    """
    weapons = load_weapons()
    return [w for w in weapons if w.type.lower() == weapon_type.lower()]


def search_weapons(query: str) -> list[Weapon]:
    """
    Search weapons by name, type, or description.
    
    Args:
        query: The search query string.
    
    Returns:
        List of weapons matching the query.
    
    Example:
        >>> results = search_weapons("dragon")
    """
    if not query:
        return load_weapons()
    
    weapons = load_weapons()
    query_lower = query.lower()
    
    results = []
    for weapon in weapons:
        # Search in name, type, description
        if (query_lower in weapon.name.lower() or
            query_lower in weapon.type.lower() or
            (weapon.description and query_lower in weapon.description.lower())):
            results.append(weapon)
            continue
        
        # Search in dropped_by
        if any(query_lower in monster.lower() for monster in weapon.dropped_by):
            results.append(weapon)
            continue
        
        # Search in NPC names (sell_to only)
        for npc_price in weapon.sell_to:
            if isinstance(npc_price, NPCPrice) and query_lower in npc_price.npc.lower():
                results.append(weapon)
                break
    
    logger.info(f"Search for '{query}' found {len(results)} weapons")
    return results


def get_weapon_types() -> list[str]:
    """
    Get all unique weapon types available.
    
    Returns:
        List of weapon type strings.
    
    Example:
        >>> types = get_weapon_types()
        >>> print(types)  # ['sword', 'axe', 'club', 'distance']
    """
    weapons = load_weapons()
    types = sorted(set(weapon.type for weapon in weapons))
    return types
