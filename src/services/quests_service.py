"""
Quests service for Fibulopedia.

This module handles loading, parsing, and querying quest data.
Supports searching by name, location, and reward.
"""

from typing import Optional

import streamlit as st

from src.config import QUESTS_FILE
from src.models import Quest
from src.services.data_loader import (
    load_json,
    validate_required_fields
)
from src.logging_utils import setup_logger

logger = setup_logger(__name__)


def load_quests() -> list[Quest]:
    """
    Load all quests from the quests.json file.
    
    Returns:
        List of Quest objects, or an empty list if loading fails.
    
    Example:
        >>> quests = load_quests()
        >>> print(f"Loaded {len(quests)} quests")
    """
    data = load_json(QUESTS_FILE)
    
    if not data or not isinstance(data, list):
        logger.warning("No quests data available or invalid format")
        return []
    
    quests = []
    for item in data:
        if not validate_required_fields(
            item,
            ["id", "name", "location", "reward"],
            "Quest"
        ):
            continue
        
        try:
            quest = Quest(
                id=str(item["id"]),
                name=str(item["name"]),
                location=str(item["location"]),
                reward=str(item["reward"]),
                min_level=int(item.get("min_level", 0)),
                short_description=item.get("short_description"),
                difficulty=item.get("difficulty"),
                steps=item.get("steps")
            )
            quests.append(quest)
        except Exception as e:
            logger.error(f"Error parsing quest {item.get('id', 'unknown')}: {e}")
    
    logger.info(f"Loaded {len(quests)} quests")
    return quests


def get_quest_by_id(quest_id: str) -> Optional[Quest]:
    """
    Get a specific quest by its ID.
    
    Args:
        quest_id: The unique ID of the quest.
    
    Returns:
        The Quest object if found, None otherwise.
    
    Example:
        >>> quest = get_quest_by_id("quest_001")
        >>> if quest:
        ...     print(quest.name)
    """
    quests = load_quests()
    for quest in quests:
        if quest.id == quest_id:
            return quest
    return None


def search_quests(query: str) -> list[Quest]:
    """
    Search quests by name, location, description, or reward.
    
    Args:
        query: The search query string.
    
    Returns:
        List of quests matching the query.
    
    Example:
        >>> results = search_quests("sword")
    """
    if not query:
        return load_quests()
    
    quests = load_quests()
    query_lower = query.lower()
    
    results = [
        quest for quest in quests
        if (query_lower in quest.name.lower() or
            query_lower in quest.location.lower() or
            query_lower in quest.short_description.lower() or
            query_lower in quest.reward.lower())
    ]
    
    logger.info(f"Search for '{query}' found {len(results)} quests")
    return results


def filter_quests_by_location(location: str) -> list[Quest]:
    """
    Filter quests by location.
    
    Args:
        location: The location to filter by.
    
    Returns:
        List of quests in the specified location.
    
    Example:
        >>> quests = filter_quests_by_location("Thais")
    """
    quests = load_quests()
    location_lower = location.lower()
    return [q for q in quests if location_lower in q.location.lower()]


def get_quest_locations() -> list[str]:
    """
    Get all unique quest locations.
    
    Returns:
        List of location strings.
    
    Example:
        >>> locations = get_quest_locations()
        >>> print(locations)
    """
    quests = load_quests()
    locations = sorted(set(quest.location for quest in quests))
    return locations
