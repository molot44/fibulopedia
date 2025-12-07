"""
Monsters page for Fibulopedia.

This page displays all monsters with their HP, EXP, loot, and locations.
Users can search monsters and plan their hunting strategies.
"""

import streamlit as st
from pathlib import Path
import os
import uuid
import streamlit_analytics2 as streamlit_analytics

from src.services.monsters_service import (
    load_monsters, 
    search_monsters, 
    get_monster_image_path,
    get_locations
)
from src.services.equipment_service import load_equipment
from src.services.weapons_service import load_weapons
from src.ui.layout import (
    setup_page_config,
    load_custom_css,
    create_page_header,
    create_sidebar_navigation,
    create_footer
)
from src.config import ASSETS_DIR, Theme
from src.logging_utils import setup_logger
from src.analytics_utils import track_page_view
import base64

logger = setup_logger(__name__)


def get_image_base64(image_path: str) -> str:
    """Convert image to base64 for embedding in HTML."""
    try:
        with open(image_path, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    except Exception as e:
        logger.error(f"Error loading image {image_path}: {e}")
        return ""

# Initialize session ID for analytics
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Start analytics tracking
streamlit_analytics.start_tracking()

# Configure page
setup_page_config("Monsters", "")
load_custom_css()
create_sidebar_navigation("Monsters")


def get_difficulty_color(difficulty: str) -> str:
    """Get color code for difficulty level."""
    colors = {
        "easy": "#50c878",
        "medium": "#ffa500",
        "hard": "#ff4444"
    }
    return colors.get(difficulty.lower(), Theme.SECONDARY_COLOR)


def get_loot_item_image_path(image_name: str) -> str:
    """Get the path to a loot item image."""
    if not image_name:
        return None
    
    image_path = ASSETS_DIR / "items" / image_name
    if image_path.exists():
        return str(image_path)
    return None


def get_item_sell_info(item_name: str):
    """Get sell_to information for a loot item by searching equipment and weapons."""
    # Load equipment and weapons
    equipment_list = load_equipment()
    weapons_list = load_weapons()
    
    # Search for item by name (case-insensitive)
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


@st.dialog("Monster Details")
def show_monster_details(monster):
    """Display detailed monster information in a modal dialog."""
    
    # Two-column layout for image and stats
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Monster image
        image_path = get_monster_image_path(monster)
        if image_path:
            st.image(image_path, width=128)
        else:
            st.write("🎭 No image available")
    
    with col2:
        # Monster name and stats
        st.markdown(f"### {monster.name}")
        st.write("")
        st.markdown(f"**💔 Health:** {monster.hp} HP")
        st.markdown(f"**✨ Experience:** {monster.exp} XP")
        
        # Summon/Convince display
        summon_text = f"{monster.summon}" if monster.summon else "-"
        convince_text = f"{monster.convince}" if monster.convince else "-"
        st.markdown(f"**🔮 Summon/Convince:** {summon_text}/{convince_text}")
    
    st.markdown("---")
    
    # Loot section
    st.markdown("### 💰 Loot")
    
    # CSS for sell tooltip
    st.markdown("""
        <style>
        .loot-item-container {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
        }
        .loot-npc-icon {
            position: relative;
            display: inline-block;
            cursor: pointer;
            color: #d4af37;
            font-weight: bold;
            font-size: 1rem;
        }
        .loot-npc-tooltip {
            visibility: hidden;
            position: absolute;
            z-index: 1000;
            background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
            border: 1px solid #d4af37;
            border-radius: 6px;
            padding: 8px 12px;
            left: 25px;
            top: -5px;
            width: max-content;
            max-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        }
        .loot-npc-icon:hover .loot-npc-tooltip {
            visibility: visible;
        }
        .loot-npc-tooltip-title {
            color: #d4af37;
            font-weight: bold;
            margin-bottom: 4px;
            font-size: 0.9rem;
        }
        .loot-npc-tooltip-item {
            color: #e0e0e0;
            font-size: 0.85rem;
            margin-left: 8px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    if monster.loot_items:
        for item in monster.loot_items:
            item_name = item.get("name", "Unknown")
            min_qty = item.get("min", 1)
            max_qty = item.get("max", 1)
            
            if min_qty == max_qty and max_qty == 1:
                qty_text = ""
            elif min_qty == max_qty:
                qty_text = f" ({max_qty}x)"
            else:
                qty_text = f" ({min_qty}-{max_qty}x)"
            
            # Get sell info for this item
            sell_info = get_item_sell_info(item_name)
            
            # Build sell tooltip HTML
            sell_icon_html = ""
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
                    tooltip_content += f'<div class="loot-npc-tooltip-title">Sell To ({price} gp)</div>'
                    for npc_info in price_groups[price]:
                        tooltip_content += f'<div class="loot-npc-tooltip-item">{npc_info}</div>'
                
                npc_count = len(sell_info)
                npc_text = "NPC" if npc_count == 1 else "NPC's"
                sell_icon_html = f'<span class="loot-npc-icon">💰 {npc_count} {npc_text}<div class="loot-npc-tooltip">{tooltip_content}</div></span>'
            
            # Display item with image and name
            item_col1, item_col2 = st.columns([1, 8])
            
            with item_col1:
                item_image = get_loot_item_image_path(item.get("image"))
                if item_image:
                    st.image(item_image, width=32)
                else:
                    st.write("📦")
            
            with item_col2:
                # Combine name and sell icon in one markdown
                if sell_icon_html:
                    # Display inline with proper spacing
                    st.markdown(f"""
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-weight: bold;">{item_name}{qty_text}</span>
                            {sell_icon_html}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"**{item_name}**{qty_text}")
    else:
        # Fallback to text loot - split by comma and display with sell info
        if monster.loot:
            loot_items = [item.strip() for item in monster.loot.split(',')]
            for loot_item in loot_items:
                # Get sell info for this item
                sell_info = get_item_sell_info(loot_item)
                
                # Build sell icon HTML
                sell_icon_html = ""
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
                        tooltip_content += f'<div class="loot-npc-tooltip-title">Sell To ({price} gp)</div>'
                        for npc_info in price_groups[price]:
                            tooltip_content += f'<div class="loot-npc-tooltip-item">{npc_info}</div>'
                    
                    npc_count = len(sell_info)
                    npc_text = "NPC" if npc_count == 1 else "NPC's"
                    sell_icon_html = f'<span class="loot-npc-icon">💰 {npc_count} {npc_text}<div class="loot-npc-tooltip">{tooltip_content}</div></span>'
                
                # Display with or without sell icon
                if sell_icon_html:
                    st.markdown(f"""
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                            <span>• <strong>{loot_item}</strong></span>
                            {sell_icon_html}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"• **{loot_item}**")
        else:
            st.write("Nothing")


def main() -> None:
    """Main function to render the monsters page."""
    logger.info("Rendering monsters page")
    
    # Track page view
    session_id = st.session_state.get("session_id")
    track_page_view("Monsters", session_id)
    
    # Check if modal should be shown
    if "show_monster_modal" in st.session_state and st.session_state.show_monster_modal:
        show_monster_details(st.session_state.selected_monster)
        st.session_state.show_monster_modal = False

    # Page header
    create_page_header(
        title="Monsters",
        subtitle="Browse creatures, view stats, and plan your hunts",
        icon=""
    )

    # Search and filter section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "Search monsters",
            placeholder="Search by name, location, or loot...",
            key="monster_search"
        )
    
    with col2:
        sort_by = st.radio(
            "Sort by",
            options=["Name", "HP", "EXP"],
            key="monster_sort",
            horizontal=False
        )

    # Load and filter monsters
    if search_query:
        monsters = search_monsters(search_query)
    else:
        monsters = load_monsters()

    if not monsters:
        st.info("No monsters found matching your criteria.")
        create_footer()
        return
    
    # Apply sorting
    if sort_by == "Name":
        monsters = sorted(monsters, key=lambda m: m.name.lower())
    elif sort_by == "HP":
        monsters = sorted(monsters, key=lambda m: m.hp, reverse=True)
    elif sort_by == "EXP":
        monsters = sorted(monsters, key=lambda m: m.exp, reverse=True)

    st.markdown(f"**Found {len(monsters)} monster(s)**")
    st.markdown("---")

    # Custom CSS for monster cards
    st.markdown("""
        <style>
        .monster-card-compact {
            background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
            border: 1px solid #444;
            border-radius: 8px;
            padding: 8px;
            min-height: 135px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            transition: all 0.2s ease;
            cursor: pointer;
        }
        .monster-card-compact:hover {
            border-color: #d4af37;
            box-shadow: 0 2px 12px rgba(212, 175, 55, 0.3);
            transform: translateY(-3px);
        }
        /* Style form submit button */
        form[data-testid="stForm"] button[type="submit"] {
            background: linear-gradient(135deg, #d4af37 0%, #b8941e 100%) !important;
            color: #1a1a1a !important;
            border: 1px solid #d4af37 !important;
            padding: 4px 8px !important;
            font-size: 0.7rem !important;
            font-weight: 600 !important;
            border-radius: 6px !important;
            transition: all 0.2s ease !important;
            margin-top: 6px !important;
            height: auto !important;
            min-height: 28px !important;
        }
        form[data-testid="stForm"] button[type="submit"]:hover {
            background: linear-gradient(135deg, #ffd700 0%, #d4af37 100%) !important;
            box-shadow: 0 2px 8px rgba(212, 175, 55, 0.4) !important;
            transform: translateY(-1px) !important;
        }
        form[data-testid="stForm"] {
            position: relative;
            margin-bottom: 8px;
        }
        /* Remove minimization */
        .monster-card-image-compact {
            width: 48px;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(0,0,0,0.4);
            border-radius: 6px;
            overflow: hidden;
            margin-bottom: 8px;
        }
        .monster-card-image-compact img {
            image-rendering: pixelated;
            max-width: 48px;
            max-height: 48px;
        }
        .monster-card-name-compact {
            font-size: 0.9rem;
            font-weight: bold;
            color: #d4af37;
            text-align: center;
            margin-bottom: 8px;
            min-height: 2.2em;
            display: flex;
            align-items: center;
            justify-content: center;
            line-height: 1.1;
        }
        .monster-card-stats-compact {
            display: flex;
            flex-direction: column;
            gap: 3px;
            margin-bottom: 6px;
            width: 100%;
        }
        .stat-compact {
            font-size: 0.7rem;
            color: #aaa;
            text-align: center;
            background: rgba(0,0,0,0.3);
            padding: 2px 4px;
            border-radius: 4px;
        }
        .monster-card-difficulty-compact {
            padding: 3px 8px;
            border-radius: 10px;
            font-size: 0.6rem;
            font-weight: bold;
            text-transform: uppercase;
            color: white;
            letter-spacing: 0.5px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Display monsters in grid format (6 per row)
    for i in range(0, len(monsters), 6):
        cols = st.columns(6)
        for j, col in enumerate(cols):
            if i + j < len(monsters):
                monster = monsters[i + j]
                
                with col:
                    # Get monster image
                    image_path = get_monster_image_path(monster)
                    difficulty_color = get_difficulty_color(monster.difficulty or "medium")
                    
                    # Get image as base64 if exists
                    image_html = ""
                    if image_path and os.path.exists(image_path):
                        img_base64 = get_image_base64(image_path)
                        if img_base64:
                            image_html = f'<img src="data:image/gif;base64,{img_base64}">'
                        else:
                            image_html = '<div style="font-size: 1.5rem;">🎭</div>'
                    else:
                        image_html = '<div style="font-size: 1.5rem;">🎭</div>'
                    
                    # Create clickable monster card using form
                    with st.form(key=f"monster_form_{monster.id}"):
                        # Create compact card HTML
                        card_html = f"""
                        <div class="monster-card-compact">
                            <div class="monster-card-image-compact">
                                {image_html}
                            </div>
                            <div class="monster-card-name-compact">{monster.name}</div>
                            <div class="monster-card-stats-compact">
                                <div class="stat-compact">HP: {monster.hp}</div>
                                <div class="stat-compact">EXP: {monster.exp}</div>
                            </div>
                        </div>
                        """
                        
                        st.markdown(card_html, unsafe_allow_html=True)
                        
                        # Submit button that covers the entire form
                        if st.form_submit_button("View", use_container_width=True):
                            st.session_state.selected_monster = monster
                            st.session_state.show_monster_modal = True
                            st.rerun()

    # Footer
    create_footer()


if __name__ == "__main__":
    try:
        main()
    finally:
        # Stop analytics tracking
        streamlit_analytics.stop_tracking()
