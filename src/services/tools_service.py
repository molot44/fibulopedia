"""
Tools service for Fibulopedia.

This module handles loading, parsing, and querying tool data.
It provides functions to get all tools, filter by type, search by name,
and retrieve individual tool details.

Version: 1.0 - Initial implementation with NPCPrice support for sell_to.
"""

from typing import Optional

import streamlit as st

from src.config import CONTENT_DIR
from src.models import Tool, NPCPrice
from src.services.data_loader import (
    load_json,
    validate_required_fields,
    safe_float,
    safe_list,
    parse_npc_prices
)
from src.logging_utils import setup_logger

logger = setup_logger(__name__)

TOOLS_FILE = CONTENT_DIR / "tools.json"


def load_tools() -> list[Tool]:
    """
    Load all tools from the tools.json file.
    
    Returns:
        List of Tool objects, or an empty list if loading fails.
    
    Example:
        >>> tools = load_tools()
        >>> print(f"Loaded {len(tools)} tools")
    """
    data = load_json(TOOLS_FILE)
    
    if not data or not isinstance(data, list):
        logger.warning("No tools data available or invalid format")
        return []
    
    tools = []
    for item in data:
        if not validate_required_fields(
            item,
            ["id", "type", "name", "weight"],
            "Tool"
        ):
            continue
        
        try:
            tool = Tool(
                id=str(item["id"]),
                type=str(item["type"]),
                name=str(item["name"]),
                weight=safe_float(item["weight"]),
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
            tools.append(tool)
        except Exception as e:
            logger.error(f"Error parsing tool {item.get('id', 'unknown')}: {e}")
    
    logger.info(f"Loaded {len(tools)} tools")
    return tools


def get_tool_by_id(tool_id: str) -> Optional[Tool]:
    """
    Get a specific tool by its ID.
    
    Args:
        tool_id: The unique ID of the tool.
    
    Returns:
        The Tool object if found, None otherwise.
    
    Example:
        >>> tool = get_tool_by_id("tool_001")
        >>> if tool:
        ...     print(tool.name)
    """
    tools = load_tools()
    for tool in tools:
        if tool.id == tool_id:
            return tool
    return None


def filter_tools_by_type(tool_type: str) -> list[Tool]:
    """
    Filter tools by their type.
    
    Args:
        tool_type: The tool type to filter by (e.g., "mining", "utility").
    
    Returns:
        List of tools matching the specified type.
    
    Example:
        >>> mining_tools = filter_tools_by_type("mining")
    """
    tools = load_tools()
    return [t for t in tools if t.type.lower() == tool_type.lower()]


def search_tools(query: str) -> list[Tool]:
    """
    Search tools by name, type, description, or NPC names.
    
    Args:
        query: The search query string.
    
    Returns:
        List of tools matching the query.
    
    Example:
        >>> results = search_tools("pick")
    """
    if not query:
        return load_tools()
    
    tools = load_tools()
    query_lower = query.lower()
    
    results = []
    for tool in tools:
        # Search in name, type, description
        if (query_lower in tool.name.lower() or
            query_lower in tool.type.lower() or
            (tool.description and query_lower in tool.description.lower())):
            results.append(tool)
            continue
        
        # Search in dropped_by
        if any(query_lower in monster.lower() for monster in tool.dropped_by):
            results.append(tool)
            continue
        
        # Search in NPC names (sell_to)
        for npc_price in tool.sell_to:
            if isinstance(npc_price, NPCPrice) and query_lower in npc_price.npc.lower():
                results.append(tool)
                break
    
    logger.info(f"Search for '{query}' found {len(results)} tools")
    return results


def get_tool_types() -> list[str]:
    """
    Get all unique tool types available.
    
    Returns:
        List of tool type strings.
    
    Example:
        >>> types = get_tool_types()
        >>> print(types)  # ['mining', 'utility', ...]
    """
    tools = load_tools()
    types = sorted(set(tool.type for tool in tools))
    return types
