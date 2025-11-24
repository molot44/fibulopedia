"""
Spells service for Fibulopedia.

This module handles loading, parsing, and querying spell data.
Supports filtering by vocation, level, and searching by various criteria.
"""

from typing import Optional

import streamlit as st

from src.config import SPELLS_FILE
from src.models import Spell
from src.services.data_loader import (
    load_json,
    validate_required_fields,
    safe_int
)
from src.logging_utils import setup_logger

logger = setup_logger(__name__)


def load_spells() -> list[Spell]:
    """
    Load all spells from the spells.json file.
    
    Returns:
        List of Spell objects, or an empty list if loading fails.
    
    Example:
        >>> spells = load_spells()
        >>> print(f"Loaded {len(spells)} spells")
    """
    data = load_json(SPELLS_FILE)
    
    if not data or not isinstance(data, list):
        logger.warning("No spells data available or invalid format")
        return []
    
    spells = []
    for item in data:
        if not validate_required_fields(
            item,
            ["id", "name", "incantation", "vocation", "level", "mana", "effect"],
            "Spell"
        ):
            continue
        
        try:
            spell = Spell(
                id=str(item["id"]),
                name=str(item["name"]),
                incantation=str(item["incantation"]),
                vocation=str(item["vocation"]),
                level=safe_int(item["level"]),
                mana=safe_int(item["mana"]),
                effect=str(item["effect"]),
                type=item.get("type"),
                spell_type=item.get("spell_type"),
                price=safe_int(item.get("price", 0)),
                magic_level_required=safe_int(item.get("magic_level_required", 0)),
                premium=bool(item.get("premium", False))
            )
            spells.append(spell)
        except Exception as e:
            logger.error(f"Error parsing spell {item.get('id', 'unknown')}: {e}")
    
    logger.info(f"Loaded {len(spells)} spells")
    return spells


def get_spell_by_id(spell_id: str) -> Optional[Spell]:
    """
    Get a specific spell by its ID.
    
    Args:
        spell_id: The unique ID of the spell.
    
    Returns:
        The Spell object if found, None otherwise.
    
    Example:
        >>> spell = get_spell_by_id("spell_001")
        >>> if spell:
        ...     print(spell.name)
    """
    spells = load_spells()
    for spell in spells:
        if spell.id == spell_id:
            return spell
    return None


def filter_spells_by_vocation(vocation: str) -> list[Spell]:
    """
    Filter spells by vocation.
    
    Args:
        vocation: The vocation to filter by (Sorcerer, Druid, Paladin, Knight, All).
    
    Returns:
        List of spells matching the specified vocation.
    
    Example:
        >>> druid_spells = filter_spells_by_vocation("Druid")
    """
    spells = load_spells()
    vocation_lower = vocation.lower()
    
    # Include spells that match the vocation or are available to "All"
    return [
        s for s in spells
        if s.vocation.lower() == vocation_lower or s.vocation.lower() == "all"
    ]


def filter_spells_by_level(min_level: int, max_level: Optional[int] = None) -> list[Spell]:
    """
    Filter spells by level range.
    
    Args:
        min_level: Minimum required level.
        max_level: Maximum level (optional). If None, no upper limit.
    
    Returns:
        List of spells within the level range.
    
    Example:
        >>> mid_level_spells = filter_spells_by_level(20, 40)
    """
    spells = load_spells()
    
    if max_level is None:
        return [s for s in spells if s.level >= min_level]
    else:
        return [s for s in spells if min_level <= s.level <= max_level]


def search_spells(query: str) -> list[Spell]:
    """
    Search spells by name, incantation, effect, or vocation.
    
    Args:
        query: The search query string.
    
    Returns:
        List of spells matching the query.
    
    Example:
        >>> results = search_spells("fire")
    """
    if not query:
        return load_spells()
    
    spells = load_spells()
    query_lower = query.lower()
    
    results = [
        spell for spell in spells
        if (query_lower in spell.name.lower() or
            query_lower in spell.incantation.lower() or
            query_lower in spell.effect.lower() or
            query_lower in spell.vocation.lower() or
            (spell.type and query_lower in spell.type.lower()))
    ]
    
    logger.info(f"Search for '{query}' found {len(results)} spells")
    return results


def get_vocations() -> list[str]:
    """
    Get all unique vocations available.
    
    Returns:
        List of vocation strings.
    
    Example:
        >>> vocations = get_vocations()
        >>> print(vocations)  # ['Sorcerer', 'Druid', 'Paladin', 'Knight', 'All']
    """
    spells = load_spells()
    vocations = sorted(set(spell.vocation for spell in spells))
    return vocations


def get_spell_types() -> list[str]:
    """
    Get all unique spell types available.
    
    Returns:
        List of spell type strings.
    
    Example:
        >>> types = get_spell_types()
        >>> print(types)  # ['offensive', 'healing', 'support', ...]
    """
    spells = load_spells()
    types = sorted(set(spell.type for spell in spells if spell.type))
    return types
