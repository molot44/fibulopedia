"""
Data loader service for Fibulopedia.

This module provides generic utilities for loading data from various file
formats (JSON, YAML, CSV) in the content directory. It handles error cases
gracefully and provides consistent error reporting.

Version: 2.0 - Added NPC data validation and parsing utilities.
"""

import json
from pathlib import Path
from typing import Any, Optional

import streamlit as st

from src.logging_utils import setup_logger

logger = setup_logger(__name__)

# Reference lists for NPC data validation
VALID_NPC_NAMES = [
    "Rashid", "Yasir", "Alesar", "Nah'Bob", "Haroun", "Alexander",
    "Brengus", "Esrik", "Flint", "Gnomally", "H.L.", "Hardek",
    "Harkath", "Henrietta", "Honna", "Ishina", "Kroox", "Lorbas",
    "Naji", "Orockwell", "Perod", "Razan", "Romella", "Sam",
    "Tamoril", "Tandros", "Tesha", "Turvy", "Uzgod", "Willard",
    "Xodet", "Yaman", "Zora", "Rowenna", "Memech", "Robert",
    "Shanar", "Ulrik"
]

VALID_LOCATIONS = [
    "Thais", "Carlin", "Venore", "Kazordoon", "Ab'Dendriel",
    "Edron", "Ankrahmun", "Port Hope", "Liberty Bay", "Svargrond",
    "Yalahar", "Gray Beach", "Fibula", "Greenshore", "Stonehome",
    "Rookgaard"
]


def load_json(file_path: Path) -> Optional[list[dict[str, Any]] | dict[str, Any]]:
    """
    Load data from a JSON file.
    
    Args:
        file_path: Path to the JSON file.
    
    Returns:
        The parsed JSON data (typically a list of dicts or a single dict),
        or None if loading fails.
    
    Raises:
        No exceptions are raised; errors are logged and None is returned.
    
    Example:
        >>> data = load_json(Path("content/weapons.json"))
        >>> if data:
        ...     print(f"Loaded {len(data)} weapons")
    """
    if not file_path.exists():
        logger.warning(f"File not found: {file_path}")
        return None
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Successfully loaded data from {file_path}")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}")
        return None


def save_json(file_path: Path, data: Any, indent: int = 2) -> bool:
    """
    Save data to a JSON file.
    
    Args:
        file_path: Path to save the JSON file.
        data: The data to serialize to JSON.
        indent: Indentation level for pretty printing.
    
    Returns:
        True if successful, False otherwise.
    
    Example:
        >>> success = save_json(Path("content/weapons.json"), weapons_data)
    """
    try:
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        
        logger.info(f"Successfully saved data to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving to {file_path}: {e}")
        return False


def validate_required_fields(
    data: dict[str, Any],
    required_fields: list[str],
    entity_name: str = "entity"
) -> bool:
    """
    Validate that all required fields are present in a data dictionary.
    
    Args:
        data: The dictionary to validate.
        required_fields: List of required field names.
        entity_name: Name of the entity type for error messages.
    
    Returns:
        True if all required fields are present, False otherwise.
    
    Example:
        >>> is_valid = validate_required_fields(
        ...     weapon_data,
        ...     ["id", "name", "attack", "defense"],
        ...     "Weapon"
        ... )
    """
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        logger.warning(
            f"{entity_name} missing required fields: {', '.join(missing_fields)}"
        )
        return False
    
    return True


def safe_int(value: Any, default: int = 0) -> int:
    """
    Safely convert a value to an integer.
    
    Args:
        value: The value to convert.
        default: Default value if conversion fails.
    
    Returns:
        The integer value or the default.
    
    Example:
        >>> hp = safe_int(monster_data.get("hp"), default=100)
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value: Any, default: float = 0.0) -> float:
    """
    Safely convert a value to a float.
    
    Args:
        value: The value to convert.
        default: Default value if conversion fails.
    
    Returns:
        The float value or the default.
    
    Example:
        >>> weight = safe_float(item_data.get("weight"), default=1.0)
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_list(value: Any, default: Optional[list] = None) -> list:
    """
    Safely convert a value to a list.
    
    Args:
        value: The value to convert.
        default: Default value if conversion fails.
    
    Returns:
        The list value or the default (empty list if default is None).
    
    Example:
        >>> dropped_by = safe_list(item_data.get("dropped_by"))
    """
    if default is None:
        default = []
    
    if isinstance(value, list):
        return value
    elif value is None:
        return default
    else:
        return [value]


def parse_npc_prices(
    npc_data: Any,
    validate: bool = True,
    item_name: str = "unknown"
) -> list:
    """
    Parse NPC price data from JSON format to NPCPrice objects.
    
    This function converts dictionaries containing NPC selling information
    into strongly-typed NPCPrice objects. It validates the data structure
    and logs warnings for invalid entries.
    
    Args:
        npc_data: Raw data from JSON (list of dicts or None).
        validate: Whether to validate NPC names and locations against known values.
        item_name: Name of the item (for logging purposes).
    
    Returns:
        List of NPCPrice objects. Returns empty list if input is invalid.
    
    Example:
        >>> npc_list = [
        ...     {"npc": "Rashid", "location": "Carlin", "price": 100},
        ...     {"npc": "Yasir", "location": "Venore", "price": 95}
        ... ]
        >>> prices = parse_npc_prices(npc_list)
        >>> print(f"Found {len(prices)} NPCs")
    """
    # Import here to avoid circular dependency
    from src.models import NPCPrice
    
    if not npc_data or not isinstance(npc_data, list):
        return []
    
    parsed_prices = []
    
    for entry in npc_data:
        if not isinstance(entry, dict):
            logger.warning(f"Invalid NPC entry for {item_name}: not a dictionary")
            continue
        
        # Extract required fields
        npc_name = entry.get("npc", "").strip()
        price = entry.get("price")
        location = entry.get("location", "").strip()
        
        # Validate required fields
        if not npc_name:
            logger.warning(f"Missing NPC name for {item_name}")
            continue
        
        if price is None:
            logger.warning(f"Missing price for {item_name} - NPC: {npc_name}")
            continue
        
        # Convert price to int
        try:
            price_int = int(price)
        except (ValueError, TypeError):
            logger.warning(f"Invalid price for {item_name} - NPC: {npc_name}, Price: {price}")
            continue
        
        # Optional validation against known NPCs and locations
        if validate:
            if npc_name not in VALID_NPC_NAMES:
                logger.info(f"Unknown NPC name: '{npc_name}' for {item_name}")
            
            if location and location not in VALID_LOCATIONS:
                logger.info(f"Unknown location: '{location}' for {item_name}")
        
        # Create NPCPrice object
        npc_price = NPCPrice(
            npc=npc_name,
            price=price_int,
            location=location
        )
        parsed_prices.append(npc_price)
    
    return parsed_prices


def validate_npc_consistency(items: list[Any], item_type: str = "item") -> list[str]:
    """
    Validate consistency of NPC names and locations across all items.
    
    This function checks that NPC names and locations are used consistently
    across all items. It returns a list of validation issues found.
    
    Args:
        items: List of item objects (Weapon, Equipment, Tool, Food) with sell_to attribute.
        item_type: Type of items being validated (for logging).
    
    Returns:
        List of validation issue strings. Empty list if no issues found.
    
    Example:
        >>> weapons = load_weapons()
        >>> issues = validate_npc_consistency(weapons, "weapon")
        >>> if issues:
        ...     for issue in issues:
        ...         print(f"Warning: {issue}")
    """
    # Import here to avoid circular dependency
    from src.models import NPCPrice
    
    npc_locations = {}
    issues = []
    
    for item in items:
        if not hasattr(item, 'sell_to'):
            continue
        
        for npc_price in item.sell_to:
            if not isinstance(npc_price, NPCPrice):
                continue
            
            if npc_price.npc not in npc_locations:
                npc_locations[npc_price.npc] = set()
            
            if npc_price.location:
                npc_locations[npc_price.npc].add(npc_price.location)
    
    # Check for NPCs in multiple locations
    for npc, locations in npc_locations.items():
        if len(locations) > 1:
            issue = f"NPC '{npc}' appears in multiple locations for {item_type}s: {', '.join(sorted(locations))}"
            logger.warning(issue)
            issues.append(issue)
    
    logger.info(f"Validated {len(npc_locations)} unique NPCs for {item_type}s")
    return issues
