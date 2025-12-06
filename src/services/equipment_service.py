"""
Equipment service for Fibulopedia.

This module handles loading, parsing, and querying equipment data.
Equipment is organized by slots (helmet, armor, legs, boots, shield, ring, amulet).

Version: 2.0 - Refactored to use NPCPrice dataclass and removed buy_from support.
"""

from typing import Optional

import streamlit as st

from src.config import EQUIPMENT_FILE
from src.models import EquipmentItem, NPCPrice
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


def load_equipment() -> list[EquipmentItem]:
    """
    Load all equipment from the equipment.json file.
    
    Returns:
        List of EquipmentItem objects, or an empty list if loading fails.
    
    Example:
        >>> equipment = load_equipment()
        >>> print(f"Loaded {len(equipment)} equipment items")
    """
    data = load_json(EQUIPMENT_FILE)
    
    if not data or not isinstance(data, list):
        logger.warning("No equipment data available or invalid format")
        return []
    
    equipment_items = []
    for item in data:
        if not validate_required_fields(
            item,
            ["id", "slot", "name", "defense", "weight"],
            "Equipment"
        ):
            continue
        
        try:
            equipment = EquipmentItem(
                id=str(item["id"]),
                slot=str(item["slot"]),
                name=str(item["name"]),
                defense=safe_int(item["defense"]),
                weight=safe_float(item["weight"]),
                image=item.get("image"),
                properties=item.get("properties"),
                dropped_by=safe_list(item.get("dropped_by")),
                sell_to=parse_npc_prices(
                    item.get("sell_to"),
                    validate=True,
                    item_name=item.get("name", "unknown")
                ),
                reward_from=safe_list(item.get("reward_from")),
                description=item.get("description")
            )
            equipment_items.append(equipment)
        except Exception as e:
            logger.error(f"Error parsing equipment {item.get('id', 'unknown')}: {e}")
    
    logger.info(f"Loaded {len(equipment_items)} equipment items")
    return equipment_items


def get_equipment_by_id(equipment_id: str) -> Optional[EquipmentItem]:
    """
    Get a specific equipment item by its ID.
    
    Args:
        equipment_id: The unique ID of the equipment.
    
    Returns:
        The EquipmentItem object if found, None otherwise.
    
    Example:
        >>> item = get_equipment_by_id("helmet_001")
        >>> if item:
        ...     print(item.name)
    """
    equipment = load_equipment()
    for item in equipment:
        if item.id == equipment_id:
            return item
    return None


def filter_equipment_by_slot(slot: str) -> list[EquipmentItem]:
    """
    Filter equipment by their slot.
    
    Args:
        slot: The equipment slot to filter by (helmet, armor, legs, etc.).
    
    Returns:
        List of equipment matching the specified slot.
    
    Example:
        >>> helmets = filter_equipment_by_slot("helmet")
    """
    equipment = load_equipment()
    return [e for e in equipment if e.slot.lower() == slot.lower()]


def search_equipment(query: str) -> list[EquipmentItem]:
    """
    Search equipment by name, slot, or description.
    
    Args:
        query: The search query string.
    
    Returns:
        List of equipment matching the query.
    
    Example:
        >>> results = search_equipment("dragon")
    """
    if not query:
        return load_equipment()
    
    equipment = load_equipment()
    query_lower = query.lower()
    
    results = []
    for item in equipment:
        # Search in name, slot, description
        if (query_lower in item.name.lower() or
            query_lower in item.slot.lower() or
            (item.description and query_lower in item.description.lower())):
            results.append(item)
            continue
        
        # Search in dropped_by
        if any(query_lower in monster.lower() for monster in item.dropped_by):
            results.append(item)
            continue
        
        # Search in NPC names (sell_to only)
        for npc_price in item.sell_to:
            if isinstance(npc_price, NPCPrice) and query_lower in npc_price.npc.lower():
                results.append(item)
                break
    
    logger.info(f"Search for '{query}' found {len(results)} equipment items")
    return results


def get_equipment_slots() -> list[str]:
    """
    Get all unique equipment slots available.
    
    Returns:
        List of equipment slot strings.
    
    Example:
        >>> slots = get_equipment_slots()
        >>> print(slots)  # ['helmet', 'armor', 'legs', 'boots', ...]
    """
    equipment = load_equipment()
    slots = sorted(set(item.slot for item in equipment))
    return slots
