# NPC Selling System Documentation

## Overview

The NPC Selling System allows tracking which NPCs buy items from players, at what price, and in which location. This system has been implemented across all item types: weapons, equipment, food, and tools.

**Version:** 2.0  
**Last Updated:** December 5, 2025

---

## Key Features

- ✅ Track multiple NPCs per item (e.g., Rashid, Yasir, Alesar)
- ✅ Different prices per NPC supported
- ✅ Location tracking for each NPC
- ✅ Type-safe implementation using `NPCPrice` dataclass
- ✅ Automatic validation of NPC names and locations
- ✅ Searchable by NPC name across all items
- ✅ Tooltip UI displaying all selling options

---

## Architecture

### Data Model (`src/models.py`)

The system uses a strongly-typed dataclass for NPC price information:

```python
@dataclass
class NPCPrice:
    """
    Represents an NPC seller and the price they offer for an item.
    
    Attributes:
        npc: Name of the NPC (e.g., "Rashid", "Yasir")
        price: Price in gold pieces that the NPC pays for the item
        location: City or location where the NPC can be found (e.g., "Thais", "Carlin")
    """
    npc: str
    price: int
    location: str = ""
```

All item dataclasses (`Weapon`, `EquipmentItem`, `Tool`, `Food`) include:

```python
sell_to: list[NPCPrice] = field(default_factory=list)
```

**Note:** The `buy_from` field has been completely removed from the system as per requirements.

---

## JSON Data Structure

### Example: weapons.json, equipment.json, tools.json

```json
{
  "id": "sword_001",
  "type": "sword",
  "name": "Dragon Slayer",
  "attack": 45,
  "defense": 25,
  "weight": 65.0,
  "hands": "One-handed",
  "image": "./assets/items/dragon_slayer.gif",
  "dropped_by": ["Dragon", "Dragon Lord"],
  "sell_to": [
    {
      "npc": "Rashid",
      "location": "Carlin",
      "price": 10000
    },
    {
      "npc": "Yasir",
      "location": "Venore",
      "price": 9500
    },
    {
      "npc": "Alesar",
      "location": "Thais",
      "price": 9000
    }
  ],
  "reward_from": [],
  "description": "A legendary sword for dragon hunting."
}
```

### Example: food.json

```json
{
  "name": "Dragon Ham",
  "image": "./assets/items/dragon_ham.gif",
  "weight": 10.0,
  "hp_gain": 200,
  "hp_per_oz": 20.0,
  "hp_per_gp": 10.0,
  "sell_to": [
    {
      "npc": "Sam",
      "location": "Thais",
      "price": 20
    }
  ]
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `npc` | string | Yes | Name of the NPC who buys the item |
| `location` | string | No | City or location where NPC can be found |
| `price` | integer | Yes | Price in gold pieces (gp) that NPC pays |

### Important Rules

1. **Empty Arrays Are Valid**: If no NPCs buy an item, use `"sell_to": []`
2. **Multiple NPCs**: You can list multiple NPCs with different prices
3. **Price Ordering**: Prices are automatically sorted (highest first) in UI
4. **Location Optional**: Location field can be empty string `""` if unknown

---

## Service Layer

### Parsing NPC Data (`src/services/data_loader.py`)

The `parse_npc_prices()` function handles conversion from JSON to `NPCPrice` objects:

```python
def parse_npc_prices(
    npc_data: Any,
    validate: bool = True,
    item_name: str = "unknown"
) -> list[NPCPrice]:
    """
    Parse NPC price data from JSON format to NPCPrice objects.
    
    Automatically validates:
    - NPC names against VALID_NPC_NAMES list
    - Locations against VALID_LOCATIONS list
    - Price values (must be valid integers)
    
    Returns empty list if data is invalid.
    """
```

### Valid NPC Names

The system validates against a predefined list of known NPCs:

```python
VALID_NPC_NAMES = [
    "Rashid", "Yasir", "Alesar", "Nah'Bob", "Haroun", "Alexander",
    "Brengus", "Esrik", "Flint", "Gnomally", "H.L.", "Hardek",
    "Harkath", "Henrietta", "Honna", "Ishina", "Kroox", "Lorbas",
    "Naji", "Orockwell", "Perod", "Razan", "Romella", "Sam",
    "Tamoril", "Tandros", "Tesha", "Turvy", "Uzgod", "Willard",
    "Xodet", "Yaman", "Zora"
]
```

### Valid Locations

```python
VALID_LOCATIONS = [
    "Thais", "Carlin", "Venore", "Kazordoon", "Ab'Dendriel",
    "Edron", "Ankrahmun", "Port Hope", "Liberty Bay", "Svargrond",
    "Yalahar", "Gray Beach", "Fibula", "Greenshore", "Stonehome",
    "Rookgaard"
]
```

**Note:** Unknown NPCs or locations will trigger an info log but won't prevent data loading.

---

## Usage Examples

### Adding Sell Data to a New Item

1. Open the appropriate JSON file (`weapons.json`, `equipment.json`, `tools.json`, or `food.json`)
2. Find or create the item entry
3. Add or update the `sell_to` array:

```json
{
  "id": "item_001",
  "name": "Example Item",
  "sell_to": [
    {
      "npc": "Rashid",
      "location": "Carlin",
      "price": 100
    }
  ]
}
```

### Multiple NPCs at Different Prices

```json
{
  "id": "valuable_sword",
  "name": "Valuable Sword",
  "sell_to": [
    {
      "npc": "Rashid",
      "location": "Carlin",
      "price": 5000
    },
    {
      "npc": "Yasir",
      "location": "Venore",
      "price": 4800
    },
    {
      "npc": "Alesar",
      "location": "Thais",
      "price": 4500
    }
  ]
}
```

The UI will group NPCs by price and display them in descending order (highest price first).

### Item Not Sold by Any NPC

```json
{
  "id": "quest_item",
  "name": "Quest Item",
  "sell_to": []
}
```

---

## UI Display

### Tooltip System

When an item has NPCs who buy it, the UI displays a badge with the count (e.g., "💰 3 NPCs"). Hovering over the badge shows a tooltip with details:

**Tooltip Structure:**
```
Sell To (5000 gp)
├─ Rashid (Carlin)

Sell To (4800 gp)
├─ Yasir (Venore)

Sell To (4500 gp)
├─ Alesar (Thais)
```

### Pages with NPC Selling Information

1. **Weapons** (`pages/Weapons.py`) - Column: "Sell To"
2. **Equipment** (`pages/Equipment.py`) - Column: "Sell To"
3. **Food** (`pages/Food.py`) - Column: "Sell To" (to be implemented)
4. **Tools** (`pages/Tools.py`) - Column: "Sell To" (to be implemented)

---

## Search Integration

The global search (`src/services/search_service.py`) includes NPC names:

- Searching for "Rashid" will return all items he buys
- Searching for "Carlin" will return items bought by NPCs in Carlin
- Works across all item types (weapons, equipment, food, tools)

---

## Validation and Consistency

### Data Validation Function

Use `validate_npc_consistency()` to check for inconsistencies:

```python
from src.services.data_loader import validate_npc_consistency
from src.services.weapons_service import load_weapons

weapons = load_weapons()
npc_report = validate_npc_consistency(weapons, "weapon")

# Returns dict: {"Rashid": {"Carlin", "Thais"}, ...}
# Warns if an NPC appears in multiple locations
```

### Common Issues

1. **Typo in NPC name**: "Rasid" instead of "Rashid"
   - System logs: `Unknown NPC name: 'Rasid' for Dragon Slayer`
   
2. **Typo in location**: "Carlien" instead of "Carlin"
   - System logs: `Unknown location: 'Carlien' for Dragon Slayer`

3. **Missing price**: NPC entry without price field
   - System logs: `Missing price for Dragon Slayer - NPC: Rashid`
   - Entry is skipped

4. **Invalid price**: Non-numeric price value
   - System logs: `Invalid price for Dragon Slayer - NPC: Rashid, Price: abc`
   - Entry is skipped

---

## Development Workflow

### Step 1: Update JSON Data

Edit the appropriate JSON file in `content/` directory:

```bash
content/
├── weapons.json
├── equipment.json
├── tools.json
└── food.json
```

### Step 2: Validate Data

Run the application and check logs for warnings:

```python
# Logs will show:
# INFO: Loaded 71 weapons
# INFO: Unknown NPC name: 'InvalidNPC' for SomeItem
```

### Step 3: Use Validation Script

Run the cleanup script to ensure consistency:

```bash
python clean_json_files.py
```

This script:
- Removes any lingering `buy_from` fields
- Ensures all items have `sell_to` field
- Reports statistics

### Step 4: Test in UI

1. Navigate to the item page (Weapons, Equipment, etc.)
2. Check that "Sell To" column displays correctly
3. Hover over NPC count badge to verify tooltip
4. Search for NPC name to test search integration

---

## Best Practices

### 1. Consistency in NPC Names

Always use the exact spelling from `VALID_NPC_NAMES`:
- ✅ `"Rashid"`
- ❌ `"rashid"` (lowercase)
- ❌ `"Rasid"` (typo)

### 2. Consistent Location Names

Always use exact location names from `VALID_LOCATIONS`:
- ✅ `"Thais"`
- ❌ `"thais"` (lowercase)
- ❌ `"Thais City"` (incorrect)

### 3. Price Values

- Use positive integers only
- Prices in gold pieces (gp)
- No decimal values
- ✅ `"price": 1000`
- ❌ `"price": "1000"` (string)
- ❌ `"price": 10.50` (decimal)

### 4. Multiple NPCs

When multiple NPCs buy the same item:
- List highest price first (optional, UI sorts automatically)
- Include location for clarity
- Use consistent NPC-location pairs

### 5. Empty Sell Data

If no NPCs buy an item:
- Always include the field: `"sell_to": []`
- Never omit the field entirely (causes warnings)

---

## Troubleshooting

### Problem: NPC data not showing in UI

**Possible Causes:**
1. JSON syntax error → Check logs for parse errors
2. Missing `sell_to` field → Add empty array
3. Invalid price format → Must be integer, not string

**Solution:**
```bash
# Check JSON validity
python -m json.tool content/weapons.json > /dev/null

# Run cleanup script
python clean_json_files.py
```

### Problem: Search not finding NPC

**Possible Causes:**
1. NPC name typo in JSON
2. Service not loading data correctly
3. Search service not updated

**Solution:**
- Verify NPC name matches `VALID_NPC_NAMES`
- Check service logs for loading errors
- Restart application to reload data

### Problem: Tooltip not appearing

**Possible Causes:**
1. Browser caching old CSS
2. JavaScript not loading
3. sell_to_tooltip not generated correctly

**Solution:**
- Hard refresh browser (Ctrl+Shift+R)
- Check browser console for JavaScript errors
- Verify tooltip HTML in page source

---

## Future Enhancements

### Potential Features

1. **Admin Interface for NPC Management**
   - Edit NPC data through UI
   - Bulk update prices
   - Import/export NPC data

2. **Price History Tracking**
   - Track price changes over time
   - Show price trends
   - Alert on significant price changes

3. **NPC Route Optimization**
   - Suggest optimal selling route
   - Calculate total profit
   - Map integration

4. **Price Comparison**
   - Compare prices across NPCs
   - Show best selling option
   - Profit calculator

5. **Data Export**
   - Export NPC data to CSV
   - Generate price reports
   - API endpoints for external tools

---

## Related Files

### Core Files
- `src/models.py` - Data models including NPCPrice
- `src/services/data_loader.py` - JSON parsing and validation
- `src/services/weapons_service.py` - Weapons data service
- `src/services/equipment_service.py` - Equipment data service
- `src/services/food_service.py` - Food data service
- `src/services/tools_service.py` - Tools data service
- `src/services/search_service.py` - Global search

### UI Files
- `pages/Weapons.py` - Weapons page with NPC tooltips
- `pages/Equipment.py` - Equipment page with NPC tooltips
- `pages/Food.py` - Food page (to be updated)
- `pages/Tools.py` - Tools page (to be updated)

### Data Files
- `content/weapons.json` - Weapons data
- `content/equipment.json` - Equipment data
- `content/tools.json` - Tools data
- `content/food.json` - Food data

### Utility Scripts
- `clean_json_files.py` - JSON cleanup utility

---

## Contact & Support

For questions or issues regarding the NPC Selling System:

1. Check application logs for detailed error messages
2. Review this documentation for common solutions
3. Validate JSON data using `clean_json_files.py`
4. Test with minimal example before full data entry

---

**Document Version:** 1.0  
**System Version:** 2.0  
**Last Updated:** December 5, 2025
