"""
Data models for Fibulopedia.

This module contains all dataclass definitions for the entities used
throughout the application. These models provide type safety and clear
structure for all data objects.

Version: 2.0 - Refactored to use NPCPrice dataclass for sell_to data.
Removed buy_from functionality as per project requirements.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class NPCPrice:
    """
    Represents an NPC seller and the price they offer for an item.
    
    This dataclass is used to store information about NPCs who buy items
    from players. It provides type safety and clear structure for trading data.
    
    Attributes:
        npc: Name of the NPC (e.g., "Rashid", "Yasir").
        price: Price in gold pieces that the NPC pays for the item.
        location: City or location where the NPC can be found (e.g., "Thais", "Carlin").
    
    Example:
        >>> npc_price = NPCPrice(npc="Rashid", price=100, location="Carlin")
        >>> print(f"{npc_price.npc} in {npc_price.location} pays {npc_price.price} gp")
        Rashid in Carlin pays 100 gp
    """
    
    npc: str
    price: int
    location: str = ""


@dataclass
class Weapon:
    """
    Represents a weapon in the game.
    
    Attributes:
        id: Unique identifier for the weapon.
        type: Type of weapon (sword, axe, club, distance).
        name: Display name of the weapon.
        attack: Attack value.
        defense: Defense value.
        weight: Weight in oz.
        hands: Number of hands required (One-handed or Two-handed).
        image: Optional path to weapon image.
        dropped_by: List of monster names that drop this weapon.
        sell_to: List of NPCPrice objects representing NPCs who buy this weapon.
        reward_from: List of quest names that reward this weapon.
        description: Optional description or special properties.
    """
    
    id: str
    type: str
    name: str
    attack: int
    defense: int
    weight: float
    hands: str = "One-handed"
    image: Optional[str] = None
    dropped_by: list[str] = field(default_factory=list)
    sell_to: list[NPCPrice] = field(default_factory=list)
    reward_from: list[str] = field(default_factory=list)
    description: Optional[str] = None


@dataclass
class EquipmentItem:
    """
    Represents an equipment item (armor, helmet, legs, boots, shield, ring, amulet).
    
    Attributes:
        id: Unique identifier for the equipment.
        slot: Equipment slot (helmet, armor, legs, boots, shield, ring, amulet).
        name: Display name of the equipment.
        defense: Defense value (or relevant stat).
        weight: Weight in oz.
        image: Optional path to equipment image.
        properties: Special properties/effects (for rings and amulets).
        dropped_by: List of monster names that drop this equipment.
        sell_to: List of NPCPrice objects representing NPCs who buy this equipment.
        reward_from: List of quest names that reward this equipment.
        description: Optional description or special properties.
    """
    
    id: str
    slot: str
    name: str
    defense: int
    weight: float
    image: Optional[str] = None
    properties: Optional[str] = None
    dropped_by: list[str] = field(default_factory=list)
    sell_to: list[NPCPrice] = field(default_factory=list)
    reward_from: list[str] = field(default_factory=list)
    description: Optional[str] = None


@dataclass
class Tool:
    """
    Represents a tool item in the game (rope, shovel, pick, etc.).
    
    Attributes:
        id: Unique identifier for the tool.
        type: Type of tool (e.g., "mining", "utility").
        name: Display name of the tool.
        weight: Weight in oz.
        image: Optional path to tool image.
        dropped_by: List of monster names that drop this tool.
        sell_to: List of NPCPrice objects representing NPCs who buy this tool.
        reward_from: List of quest names that reward this tool.
        description: Optional description of the tool's use.
    """
    
    id: str
    type: str
    name: str
    weight: float
    image: Optional[str] = None
    dropped_by: list[str] = field(default_factory=list)
    sell_to: list[NPCPrice] = field(default_factory=list)
    reward_from: list[str] = field(default_factory=list)
    description: Optional[str] = None


@dataclass
class Spell:
    """
    Represents a spell in the game.
    
    Attributes:
        id: Unique identifier for the spell.
        name: Display name of the spell.
        incantation: The magic words to cast the spell.
        vocation: Required vocation (Sorcerer, Druid, Paladin, Knight, or "All").
        level: Required level to use the spell.
        mana: Mana cost to cast the spell.
        effect: Description of what the spell does.
        type: Type of spell (offensive, healing, support, summon, etc.).
        spell_type: Spell category (instant or rune).
        price: Price to learn the spell or buy the rune (in gold pieces).
        magic_level_required: Magic level required to use the spell (for runes).
        premium: Whether the spell requires premium account.
    """
    
    id: str
    name: str
    incantation: str
    vocation: str
    level: int
    mana: int
    effect: str
    type: Optional[str] = None
    spell_type: Optional[str] = None
    price: int = 0
    magic_level_required: int = 0
    premium: bool = False


@dataclass
class Monster:
    """
    Represents a monster in the game.
    
    Attributes:
        id: Unique identifier for the monster.
        name: Display name of the monster.
        hp: Hit points.
        exp: Experience points awarded when killed.
        loot: Description or list of loot items.
        location: Spawn location or area.
        difficulty: Optional difficulty rating (easy, medium, hard).
        image: Optional filename for monster image (e.g., 'rat.gif').
        summon: Optional mana cost to summon this creature.
        convince: Optional mana cost to convince this creature.
        loot_items: Structured loot data with items and quantities.
    """
    
    id: str
    name: str
    hp: int
    exp: int
    loot: str
    location: str
    difficulty: Optional[str] = None
    image: Optional[str] = None
    summon: Optional[int] = None
    convince: Optional[int] = None
    loot_items: list[dict[str, str | int]] = field(default_factory=list)


@dataclass
class Quest:
    """
    Represents a quest in the game.
    
    Attributes:
        id: Unique identifier for the quest.
        name: Display name of the quest.
        location: Where the quest starts or takes place.
        reward: Description of the quest reward.
        min_level: Minimum level required to complete the quest.
        short_description: Brief description of the quest (optional, legacy).
        difficulty: Optional difficulty rating (legacy).
        steps: Optional list of quest steps (for future expansion).
    """
    
    id: str
    name: str
    location: str
    reward: str
    min_level: int = 0
    short_description: Optional[str] = None
    difficulty: Optional[str] = None
    steps: Optional[list[str]] = None


@dataclass
class ServerInfo:
    """
    Represents server information.
    
    Attributes:
        id: Unique identifier for the server info entry.
        name: Server name.
        description: General description of the server.
        rates: Dictionary of server rates (exp, loot, skill, magic).
        version: Client version.
        website: Server website URL.
        discord: Discord server URL.
        additional_info: Any additional information or rules.
    """
    
    id: str
    name: str
    description: str
    rates: dict[str, float | int]
    version: str
    website: Optional[str] = None
    discord: Optional[str] = None
    additional_info: Optional[str] = None


@dataclass
class SearchResult:
    """
    Represents a single search result.
    
    Attributes:
        entity_type: Type of entity (weapon, equipment, spell, monster, quest).
        entity_id: The unique ID of the entity.
        name: Display name of the entity.
        snippet: Short context snippet showing why this matched.
        page_route: The page route for navigation (e.g., "pages/Weapons.py").
        image_base64: Base64 encoded image data (optional, for weapons/equipment).
        score: Relevance score (optional, for future ranking).
    """
    
    entity_type: str
    entity_id: str
    name: str
    snippet: Optional[str] = None
    page_route: Optional[str] = None
    image_base64: Optional[str] = None
    score: Optional[float] = None


@dataclass
class MapInfo:
    """
    Represents map information.
    
    Attributes:
        id: Unique identifier.
        name: Map name.
        description: Description of the map.
        image_path: Path to the map image.
        regions: Optional list of regions/areas (for future expansion).
    """
    
    id: str
    name: str
    description: str
    image_path: str
    regions: Optional[list[dict[str, str]]] = None


@dataclass
class Food:
    """
    Represents a food item in the game.
    
    Attributes:
        name: Display name of the food.
        image: Optional path to food image.
        weight: Weight in oz (can be None for unknown values).
        hp_gain: Total HP restored by consuming (can be None for unknown values).
        hp_per_oz: HP restored per oz of weight (can be None for unknown values).
        hp_per_gp: HP restored per gold piece of value (can be None for unknown values).
        sell_to: List of NPCPrice objects representing NPCs who buy this food.
    """
    
    name: str
    image: Optional[str] = None
    weight: Optional[float] = None
    hp_gain: Optional[int] = None
    hp_per_oz: Optional[float] = None
    hp_per_gp: Optional[float] = None
    sell_to: list[NPCPrice] = field(default_factory=list)
