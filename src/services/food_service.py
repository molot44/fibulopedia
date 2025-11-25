"""
Food service for Fibulopedia.

This module handles loading, parsing, and querying food data.
It provides functions to get all food items, search by name,
and retrieve individual food item details.
"""

from typing import Optional

import streamlit as st

from src.config import CONTENT_DIR
from src.models import Food
from src.services.data_loader import (
    load_json,
    safe_int,
    safe_float
)
from src.logging_utils import setup_logger

logger = setup_logger(__name__)

FOOD_FILE = CONTENT_DIR / "food.json"


def load_food() -> list[Food]:
    """
    Load all food items from the food.json file.
    
    Returns:
        List of Food objects, or an empty list if loading fails.
    
    Example:
        >>> food_items = load_food()
        >>> print(f"Loaded {len(food_items)} food items")
    """
    data = load_json(FOOD_FILE)
    
    if not data or not isinstance(data, list):
        logger.warning("No food data available or invalid format")
        return []
    
    food_items = []
    for item in data:
        if not item.get("name"):
            logger.warning("Food item missing required field: name")
            continue
        
        try:
            # Handle null values in the data
            weight = safe_float(item.get("weight")) if item.get("weight") is not None else None
            hp_gain = safe_int(item.get("hp_gain")) if item.get("hp_gain") is not None else None
            hp_per_oz = safe_float(item.get("hp_per_oz")) if item.get("hp_per_oz") is not None else None
            hp_per_gp = safe_float(item.get("hp_per_gp")) if item.get("hp_per_gp") is not None else None
            
            food = Food(
                name=str(item["name"]),
                image=item.get("image"),
                weight=weight,
                hp_gain=hp_gain,
                hp_per_oz=hp_per_oz,
                hp_per_gp=hp_per_gp
            )
            food_items.append(food)
        except Exception as e:
            logger.error(f"Error parsing food item {item.get('name', 'unknown')}: {e}")
    
    logger.info(f"Loaded {len(food_items)} food items")
    return food_items


def get_food_by_name(name: str) -> Optional[Food]:
    """
    Get a specific food item by its name.
    
    Args:
        name: The name of the food item.
    
    Returns:
        The Food object if found, None otherwise.
    
    Example:
        >>> food = get_food_by_name("Ham")
        >>> if food:
        ...     print(food.hp_gain)
    """
    food_items = load_food()
    for food in food_items:
        if food.name.lower() == name.lower():
            return food
    return None


def search_food(query: str) -> list[Food]:
    """
    Search food items by name.
    
    Args:
        query: The search query string.
    
    Returns:
        List of food items matching the query.
    
    Example:
        >>> results = search_food("mushroom")
    """
    if not query:
        return load_food()
    
    food_items = load_food()
    query_lower = query.lower()
    
    results = []
    for food in food_items:
        # Search in name
        if query_lower in food.name.lower():
            results.append(food)
    
    logger.info(f"Search for '{query}' found {len(results)} food items")
    return results
