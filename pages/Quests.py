"""
Quests page for Fibulopedia.

This page displays all available quests with their locations and rewards.
"""

import streamlit as st
import re
import base64
import os
import uuid
import streamlit_analytics2 as streamlit_analytics

from src.services.quests_service import load_quests
from src.services.equipment_service import load_equipment
from src.services.weapons_service import load_weapons
from src.ui.layout import (
    setup_page_config,
    load_custom_css,
    create_page_header,
    create_sidebar_navigation,
    create_footer
)
from src.config import ASSETS_DIR
from src.logging_utils import setup_logger
from src.analytics_utils import track_page_view

logger = setup_logger(__name__)

# Initialize session ID for analytics
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Start analytics tracking
streamlit_analytics.start_tracking()

# Configure page
setup_page_config("Quests", "📜")
load_custom_css()
create_sidebar_navigation("Quests")


def get_spoiler_icon_base64():
    """Get spoiler icon as base64 for embedding in HTML."""
    icon_path = ASSETS_DIR / "items" / "Parchment_of_Interest.gif"
    try:
        with open(icon_path, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode()
            return f"data:image/gif;base64,{encoded}"
    except Exception as e:
        logger.error(f"Error loading spoiler icon: {e}")
        return ""


def get_item_sell_info(item_name: str):
    """Get sell_to information for an item by searching equipment and weapons."""
    equipment_list = load_equipment()
    weapons_list = load_weapons()
    
    item_name_lower = item_name.lower()
    
    # Check equipment
    for eq in equipment_list:
        if eq.name.lower() == item_name_lower and eq.sell_to and len(eq.sell_to) > 0:
            return eq.sell_to
    
    # Check weapons
    for weapon in weapons_list:
        if weapon.name.lower() == item_name_lower and weapon.sell_to and len(weapon.sell_to) > 0:
            return weapon.sell_to
    
    return None


def parse_reward_items(reward_text: str):
    """Parse reward text and extract individual items."""
    if not reward_text:
        return []
    
    # Split by common delimiters: comma, "and", "or"
    items = re.split(r',|\band\b|\bor\b', reward_text)
    
    parsed_items = []
    for item in items:
        item = item.strip()
        if not item:
            continue
        
        # Remove quantity prefixes like "2x", "5 ", etc.
        item_clean = re.sub(r'^\d+\s*x?\s*', '', item)
        item_clean = re.sub(r'^\d+\s+', '', item_clean)
        
        # Remove common suffixes like "(Book)", "gp", etc.
        item_clean = re.sub(r'\s*\([^)]*\)', '', item_clean)
        item_clean = re.sub(r'\s+gp$', '', item_clean, flags=re.IGNORECASE)
        item_clean = re.sub(r'\s+oz\.?$', '', item_clean)
        
        # Skip items that are clearly not equipment/weapons
        skip_words = ['key', 'bag', 'platinum coins', 'cookies', 'achievement', 'addon', 'outfits']
        if any(skip in item_clean.lower() for skip in skip_words):
            continue
        
        item_clean = item_clean.strip()
        if len(item_clean) > 2:  # Skip very short items
            parsed_items.append(item_clean)
    
    return parsed_items


def build_reward_html(reward_text: str):
    """Build HTML for reward column with sell icons."""
    if not reward_text:
        return ""
    
    # Parse reward items
    items = parse_reward_items(reward_text)
    
    # Build HTML with sell icons
    result_html = reward_text
    
    for item_name in items:
        sell_info = get_item_sell_info(item_name)
        if sell_info:
            # Group by price
            price_groups = {}
            for npc_price in sell_info:
                price = npc_price.price
                if price not in price_groups:
                    price_groups[price] = []
                npc_info = f"{npc_price.npc}"
                if npc_price.location:
                    npc_info += f" ({npc_price.location})"
                price_groups[price].append(npc_info)
            
            # Build tooltip content
            tooltip_content = ""
            for price in sorted(price_groups.keys(), reverse=True):
                tooltip_content += f'<div style="color: #d4af37; font-weight: bold; margin-top: 4px;">Sell To ({price} gp)</div>'
                for npc_info in price_groups[price]:
                    tooltip_content += f'<div style="color: #e0e0e0; font-size: 0.85rem; margin-left: 8px;">{npc_info}</div>'
            
            npc_count = len(sell_info)
            npc_text = "NPC" if npc_count == 1 else "NPC's"
            
            # Create sell icon with tooltip
            sell_icon = f'''<span style="position: relative; display: inline-block; cursor: pointer; color: #d4af37; font-weight: bold; font-size: 0.85rem; margin-left: 4px;" class="quest-sell-icon">
                💰 {npc_count} {npc_text}
                <div class="quest-sell-tooltip">{tooltip_content}</div>
            </span>'''
            
            # Try to inject icon after the item name in the original text
            # Use word boundaries to match whole words only
            pattern = r'\b' + re.escape(item_name) + r'\b'
            result_html = re.sub(pattern, f'{item_name}{sell_icon}', result_html, count=1, flags=re.IGNORECASE)
    
    return result_html


def main() -> None:
    """Main function to render the quests page."""
    logger.info("Rendering quests page")
    
    # Track page view
    session_id = st.session_state.get("session_id")
    track_page_view("Quests", session_id)

    # Page header
    create_page_header(
        title="Quests",
        subtitle="Complete quest list with locations, rewards, and item values",
        icon=""
    )

    # Load quests
    quests = load_quests()
    
    if not quests:
        st.warning("No quests data available.")
        create_footer()
        return

    # Search
    search_query = st.text_input(
        "Search quests",
        placeholder="Search by name, location, or reward...",
        key="quest_search"
    )

    # Filter quests
    filtered_quests = quests
    if search_query:
        search_lower = search_query.lower()
        filtered_quests = [
            q for q in quests
            if search_lower in q.name.lower()
            or search_lower in q.location.lower()
            or search_lower in q.reward.lower()
        ]

    st.markdown(f"**Found {len(filtered_quests)} quest(s)**")
    st.markdown("---")

    # Custom CSS for quest table
    st.markdown("""
        <style>
        .quest-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
        }
        .quest-table th {
            background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
            color: #d4af37;
            padding: 12px;
            text-align: left;
            border: 1px solid #444;
            font-weight: bold;
            cursor: pointer;
            user-select: none;
            position: relative;
        }
        .quest-table th.sortable:hover {
            background: linear-gradient(135deg, #3d3d3d 0%, #2a2a2a 100%);
        }
        .quest-table th.sortable::after {
            content: '';
            margin-left: 8px;
            opacity: 0.3;
        }
        .quest-table th.sortable.sorted-asc::after {
            content: '▲';
            opacity: 1;
        }
        .quest-table th.sortable.sorted-desc::after {
            content: '▼';
            opacity: 1;
        }
        .quest-table th.not-sortable {
            cursor: default;
        }
        .quest-table th.not-sortable:hover {
            background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
        }
        .quest-table td {
            padding: 10px 12px;
            border: 1px solid #333;
            color: #e0e0e0;
            vertical-align: top;
        }
        .quest-table tr:nth-child(even) {
            background: rgba(30,30,30,0.5);
        }
        .quest-table tr:hover {
            background: rgba(212,175,55,0.1);
        }
        .quest-name {
            color: #d4af37;
            font-weight: bold;
            font-size: 1rem;
        }
        .quest-min-level {
            color: #50c878;
            font-weight: bold;
        }
        .quest-location {
            color: #aaa;
            font-size: 0.9rem;
        }
        .quest-reward {
            color: #e0e0e0;
            font-size: 0.9rem;
            line-height: 1.5;
        }
        .quest-sell-icon {
            white-space: nowrap;
        }
        .quest-sell-tooltip {
            visibility: hidden;
            position: absolute;
            z-index: 1000;
            background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
            border: 1px solid #d4af37;
            border-radius: 6px;
            padding: 8px 12px;
            left: 0;
            top: 25px;
            width: max-content;
            max-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        }
        .quest-sell-icon:hover .quest-sell-tooltip {
            visibility: visible;
        }
        .quest-spoiler-link {
            display: inline-block;
            transition: transform 0.2s;
        }
        .quest-spoiler-link:hover {
            transform: scale(1.1);
        }
        </style>
    """, unsafe_allow_html=True)

    # Build table HTML with sortable headers
    table_html = '<table class="quest-table" id="questTable"><thead><tr>'
    table_html += '<th class="sortable" data-column="0">Quest Name</th>'
    table_html += '<th class="not-sortable" style="width: 60px; text-align: center;">Spoiler</th>'
    table_html += '<th class="sortable" style="width: 80px; text-align: center;" data-column="2">Min Level</th>'
    table_html += '<th class="sortable" style="width: 25%;" data-column="3">Location</th>'
    table_html += '<th class="not-sortable" style="width: 40%;">Reward</th>'
    table_html += '</tr></thead><tbody>'

    # Get spoiler icon once
    spoiler_icon = get_spoiler_icon_base64()

    for quest in filtered_quests:
        reward_html = build_reward_html(quest.reward)
        min_level_display = quest.min_level if quest.min_level > 0 else "-"
        
        # Build wiki link - replace spaces with underscores
        wiki_name = quest.name.replace(" ", "_")
        wiki_url = f"https://tibia.fandom.com/wiki/{wiki_name}"
        
        table_html += '<tr>'
        table_html += f'<td><span class="quest-name">{quest.name}</span></td>'
        table_html += f'<td style="text-align: center;"><a href="{wiki_url}" target="_blank" class="quest-spoiler-link"><img src="{spoiler_icon}" width="24" alt="Spoiler" title="View quest details on Tibia Wiki"></a></td>'
        table_html += f'<td style="text-align: center;"><span class="quest-min-level">{min_level_display}</span></td>'
        table_html += f'<td><span class="quest-location">{quest.location}</span></td>'
        table_html += f'<td><span class="quest-reward">{reward_html}</span></td>'
        table_html += '</tr>'

    table_html += '</tbody></table>'

    st.markdown(table_html, unsafe_allow_html=True)

    # Add JavaScript for client-side sorting (same as Weapons page)
    st.components.v1.html("""
    <script>
    (function() {
        function sortTable() {
            const table = window.parent.document.getElementById('questTable');
            
            if (!table) {
                setTimeout(sortTable, 100);
                return;
            }
            
            const headers = table.querySelectorAll('th.sortable');
            const sortDirections = {};
            
            headers.forEach((header, index) => {
                const columnIndex = parseInt(header.getAttribute('data-column'));
                sortDirections[columnIndex] = true; // true = ascending
                
                header.addEventListener('click', function() {
                    const columnIndex = parseInt(this.getAttribute('data-column'));
                    const tbody = table.querySelector('tbody');
                    const rows = Array.from(tbody.querySelectorAll('tr'));
                    
                    // Sort rows
                    rows.sort((a, b) => {
                        let aValue = a.cells[columnIndex].textContent.trim();
                        let bValue = b.cells[columnIndex].textContent.trim();
                        
                        // Try to parse as numbers
                        const aNum = parseFloat(aValue.replace(/[^0-9.-]/g, ''));
                        const bNum = parseFloat(bValue.replace(/[^0-9.-]/g, ''));
                        
                        if (!isNaN(aNum) && !isNaN(bNum)) {
                            return sortDirections[columnIndex] ? aNum - bNum : bNum - aNum;
                        }
                        
                        // String comparison
                        const comparison = aValue.localeCompare(bValue);
                        return sortDirections[columnIndex] ? comparison : -comparison;
                    });
                    
                    // Clear tbody
                    tbody.innerHTML = '';
                    
                    // Add sorted rows
                    rows.forEach(row => tbody.appendChild(row));
                    
                    // Update sort indicators
                    headers.forEach(h => h.classList.remove('sorted-asc', 'sorted-desc'));
                    this.classList.add(sortDirections[columnIndex] ? 'sorted-asc' : 'sorted-desc');
                    
                    // Toggle direction
                    sortDirections[columnIndex] = !sortDirections[columnIndex];
                });
            });
        }
        
        sortTable();
    })();
    </script>
    """, height=0)

    # Footer
    create_footer()


if __name__ == "__main__":
    try:
        main()
    finally:
        # Stop analytics tracking
        streamlit_analytics.stop_tracking()

