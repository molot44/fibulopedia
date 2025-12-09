"""
Search service for Fibulopedia.

This module provides global search functionality across all content types:
weapons, equipment, spells, monsters, quests, food, and tools. It returns unified
search results with entity type, name, and snippet information.

Version: 2.0 - Added food and tools search support.
"""

import os
import base64
from pathlib import Path

from src.config import MAX_SEARCH_RESULTS, SEARCH_SNIPPET_LENGTH
from src.models import SearchResult
from src.services import (
    weapons_service,
    equipment_service,
    spells_service,
    monsters_service,
    quests_service,
    food_service,
    tools_service
)
from src.logging_utils import setup_logger

logger = setup_logger(__name__)


def get_image_base64(image_path: str) -> str:
    """
    Convert an image file to base64 data URL.
    
    Args:
        image_path: Relative path to the image (e.g., "./assets/items/weapons/axe.gif").
    
    Returns:
        Base64 data URL string or empty string if loading fails.
    """
    try:
        # Get project root (3 levels up from this file)
        base_path = Path(__file__).parent.parent.parent
        # Clean path and construct full path
        clean_path = image_path.replace("./", "")
        full_path = base_path / clean_path
        
        if full_path.exists():
            with open(full_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
                ext = full_path.suffix[1:]  # Remove the dot
                return f"data:image/{ext};base64,{encoded}"
    except Exception as e:
        logger.debug(f"Failed to load image {image_path}: {e}")
    
    return ""


def get_page_route(entity_type: str) -> str:
    """
    Get the page route for a given entity type.
    
    Args:
        entity_type: The type of entity (weapon, equipment, spell, etc.).
    
    Returns:
        The page route string for st.switch_page().
    """
    page_mapping = {
        "weapon": "pages/Weapons.py",
        "equipment": "pages/Equipment.py",
        "spell": "pages/Spells.py",
        "monster": "pages/Monsters.py",
        "quest": "pages/Quests.py",
        "food": "pages/Food.py",
        "tool": "pages/Tools.py",
        "calculator": "pages/Training_Calculator.py",
        "experience": "pages/Experience_Table.py",
        "server": "pages/Server_Info.py",
        "travel": "pages/Travel_Calculator.py",
        "magic": "pages/Magic_Damage_Calculator.py"
    }
    return page_mapping.get(entity_type.lower(), "pages/Home.py")


def create_snippet(text: str, query: str, max_length: int = SEARCH_SNIPPET_LENGTH) -> str:
    """
    Create a snippet of text centered around the query match.
    
    Args:
        text: The full text to extract a snippet from.
        query: The search query to center the snippet around.
        max_length: Maximum length of the snippet.
    
    Returns:
        A snippet string with the query highlighted in context.
    
    Example:
        >>> snippet = create_snippet("This is a long text about dragons", "dragon", 30)
        >>> print(snippet)  # "...text about dragons"
    """
    if not text or not query:
        return text[:max_length] if text else ""
    
    text_lower = text.lower()
    query_lower = query.lower()
    
    # Find the position of the query in the text
    pos = text_lower.find(query_lower)
    
    if pos == -1:
        # Query not found, return beginning of text
        return text[:max_length] + ("..." if len(text) > max_length else "")
    
    # Calculate snippet boundaries
    half_length = max_length // 2
    start = max(0, pos - half_length)
    end = min(len(text), pos + len(query) + half_length)
    
    snippet = text[start:end]
    
    # Add ellipsis if needed
    if start > 0:
        snippet = "..." + snippet
    if end < len(text):
        snippet = snippet + "..."
    
    return snippet


def search_all(query: str) -> list[SearchResult]:
    """
    Search across all content types (weapons, equipment, spells, monsters, quests, food, tools).
    
    Args:
        query: The search query string.
    
    Returns:
        List of SearchResult objects, limited by MAX_SEARCH_RESULTS.
    
    Example:
        >>> results = search_all("dragon")
        >>> for result in results:
        ...     print(f"{result.entity_type}: {result.name}")
    """
    if not query or len(query.strip()) == 0:
        logger.warning("Empty search query provided")
        return []
    
    results: list[SearchResult] = []
    query_lower = query.lower()
    
    # Search weapons
    try:
        weapons = weapons_service.search_weapons(query)
        for weapon in weapons[:MAX_SEARCH_RESULTS // 7]:
            snippet_text = f"Type: {weapon.type}, Attack: {weapon.attack}, Defense: {weapon.defense}"
            if weapon.description:
                snippet_text = weapon.description
            
            # Load image if available
            image_b64 = ""
            if hasattr(weapon, 'image') and weapon.image:
                image_b64 = get_image_base64(weapon.image)
            
            results.append(SearchResult(
                entity_type="weapon",
                entity_id=weapon.id,
                name=weapon.name,
                snippet=create_snippet(snippet_text, query),
                page_route=get_page_route("weapon"),
                image_base64=image_b64
            ))
    except Exception as e:
        logger.error(f"Error searching weapons: {e}")
    
    # Search equipment
    try:
        equipment = equipment_service.search_equipment(query)
        for item in equipment[:MAX_SEARCH_RESULTS // 7]:
            snippet_text = f"Slot: {item.slot}, Defense: {item.defense}"
            if item.description:
                snippet_text = item.description
            
            # Load image if available
            image_b64 = ""
            if hasattr(item, 'image') and item.image:
                image_b64 = get_image_base64(item.image)
            
            results.append(SearchResult(
                entity_type="equipment",
                entity_id=item.id,
                name=item.name,
                snippet=create_snippet(snippet_text, query),
                page_route=get_page_route("equipment"),
                image_base64=image_b64
            ))
    except Exception as e:
        logger.error(f"Error searching equipment: {e}")
    
    # Search spells
    try:
        spells = spells_service.search_spells(query)
        for spell in spells[:MAX_SEARCH_RESULTS // 7]:
            snippet_text = f"Incantation: {spell.incantation}, Vocation: {spell.vocation}, Effect: {spell.effect}"
            
            results.append(SearchResult(
                entity_type="spell",
                entity_id=spell.id,
                name=spell.name,
                snippet=create_snippet(snippet_text, query),
                page_route=get_page_route("spell")
            ))
    except Exception as e:
        logger.error(f"Error searching spells: {e}")
    
    # Search monsters
    try:
        monsters = monsters_service.search_monsters(query)
        for monster in monsters[:MAX_SEARCH_RESULTS // 7]:
            snippet_text = f"HP: {monster.hp}, EXP: {monster.exp}, Location: {monster.location}, Loot: {monster.loot}"
            
            # Load image if available
            image_b64 = ""
            if hasattr(monster, 'image') and monster.image:
                # Monster images are in assets/monsters/ folder
                monster_image_path = f"./assets/monsters/{monster.image}"
                image_b64 = get_image_base64(monster_image_path)
            
            results.append(SearchResult(
                entity_type="monster",
                entity_id=monster.id,
                name=monster.name,
                snippet=create_snippet(snippet_text, query),
                page_route=get_page_route("monster"),
                image_base64=image_b64
            ))
    except Exception as e:
        logger.error(f"Error searching monsters: {e}")
    
    # Search quests
    try:
        quests = quests_service.search_quests(query)
        for quest in quests[:MAX_SEARCH_RESULTS // 7]:
            snippet_text = f"Location: {quest.location}, {quest.short_description}"
            
            results.append(SearchResult(
                entity_type="quest",
                entity_id=quest.id,
                name=quest.name,
                snippet=create_snippet(snippet_text, query),
                page_route=get_page_route("quest")
            ))
    except Exception as e:
        logger.error(f"Error searching quests: {e}")
    
    # Search food
    try:
        food_items = food_service.search_food(query)
        for food in food_items[:MAX_SEARCH_RESULTS // 7]:
            snippet_text = f"HP Gain: {food.hp_gain or 'N/A'}, Weight: {food.weight or 'N/A'} oz"
            
            # Load image if available
            image_b64 = ""
            if hasattr(food, 'image') and food.image:
                image_b64 = get_image_base64(food.image)
            
            results.append(SearchResult(
                entity_type="food",
                entity_id=food.name,  # Food uses name as ID
                name=food.name,
                snippet=create_snippet(snippet_text, query),
                page_route=get_page_route("food"),
                image_base64=image_b64
            ))
    except Exception as e:
        logger.error(f"Error searching food: {e}")
    
    # Search tools
    try:
        tools = tools_service.search_tools(query)
        for tool in tools[:MAX_SEARCH_RESULTS // 7]:
            snippet_text = f"Type: {tool.type}, Weight: {tool.weight} oz"
            if tool.description:
                snippet_text = tool.description
            
            # Load image if available
            image_b64 = ""
            if hasattr(tool, 'image') and tool.image:
                image_b64 = get_image_base64(tool.image)
            
            results.append(SearchResult(
                entity_type="tool",
                entity_id=tool.id,
                name=tool.name,
                snippet=create_snippet(snippet_text, query),
                page_route=get_page_route("tool"),
                image_base64=image_b64
            ))
    except Exception as e:
        logger.error(f"Error searching tools: {e}")
    
    # Limit total results
    results = results[:MAX_SEARCH_RESULTS]
    
    logger.info(f"Global search for '{query}' found {len(results)} total results")
    return results


def search_by_entity_type(query: str, entity_type: str) -> list[SearchResult]:
    """
    Search within a specific entity type.
    
    Args:
        query: The search query string.
        entity_type: The type to search (weapon, equipment, spell, monster, quest, food, tool).
    
    Returns:
        List of SearchResult objects for the specified entity type.
    
    Example:
        >>> results = search_by_entity_type("fire", "spell")
    """
    entity_type = entity_type.lower()
    
    if entity_type == "weapon":
        weapons = weapons_service.search_weapons(query)
        return [
            SearchResult(
                entity_type="weapon",
                entity_id=w.id,
                name=w.name,
                snippet=f"Type: {w.type}, Attack: {w.attack}, Defense: {w.defense}",
                page_route=get_page_route("weapon")
            )
            for w in weapons
        ]
    
    elif entity_type == "equipment":
        equipment = equipment_service.search_equipment(query)
        return [
            SearchResult(
                entity_type="equipment",
                entity_id=e.id,
                name=e.name,
                snippet=f"Slot: {e.slot}, Defense: {e.defense}",
                page_route=get_page_route("equipment")
            )
            for e in equipment
        ]
    
    elif entity_type == "spell":
        spells = spells_service.search_spells(query)
        return [
            SearchResult(
                entity_type="spell",
                entity_id=s.id,
                name=s.name,
                snippet=f"Incantation: {s.incantation}, Vocation: {s.vocation}",
                page_route=get_page_route("spell")
            )
            for s in spells
        ]
    
    elif entity_type == "monster":
        monsters = monsters_service.search_monsters(query)
        return [
            SearchResult(
                entity_type="monster",
                entity_id=m.id,
                name=m.name,
                snippet=f"HP: {m.hp}, EXP: {m.exp}, Location: {m.location}",
                page_route=get_page_route("monster")
            )
            for m in monsters
        ]
    
    elif entity_type == "quest":
        quests = quests_service.search_quests(query)
        return [
            SearchResult(
                entity_type="quest",
                entity_id=q.id,
                name=q.name,
                snippet=f"Location: {q.location}",
                page_route=get_page_route("quest")
            )
            for q in quests
        ]
    
    elif entity_type == "food":
        food_items = food_service.search_food(query)
        return [
            SearchResult(
                entity_type="food",
                entity_id=f.name,
                name=f.name,
                snippet=f"HP Gain: {f.hp_gain or 'N/A'}, Weight: {f.weight or 'N/A'} oz",
                page_route=get_page_route("food")
            )
            for f in food_items
        ]
    
    elif entity_type == "tool":
        tools = tools_service.search_tools(query)
        return [
            SearchResult(
                entity_type="tool",
                entity_id=t.id,
                name=t.name,
                snippet=f"Type: {t.type}, Weight: {t.weight} oz",
                page_route=get_page_route("tool")
            )
            for t in tools
        ]
    
    else:
        logger.warning(f"Unknown entity type for search: {entity_type}")
        return []
