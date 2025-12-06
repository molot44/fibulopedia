"""
Weapons page for Fibulopedia.

This page displays all weapons with sortable tables and filtering options.
Users can view weapon stats, search by name or type, and see where to obtain them.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import base64
import os

from src.services.weapons_service import load_weapons, search_weapons, get_weapon_types
from src.ui.layout import (
    setup_page_config,
    load_custom_css,
    create_page_header,
    create_sidebar_navigation,
    create_footer
)
from src.ui.components import create_detail_section, create_type_badge
from src.logging_utils import setup_logger

logger = setup_logger(__name__)


def get_image_as_base64(image_path: str) -> str:
    """Convert an image file to base64 string."""
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as f:
                data = f.read()
                encoded = base64.b64encode(data).decode()
                ext = os.path.splitext(image_path)[1][1:]  # Get extension without dot
                return f"data:image/{ext};base64,{encoded}"
    except Exception as e:
        logger.error(f"Error loading image {image_path}: {e}")
    return ""

# Configure page
setup_page_config("Weapons", "")
load_custom_css()
create_sidebar_navigation("Weapons")


def main() -> None:
    """Main function to render the weapons page."""
    logger.info("Rendering weapons page")

    # Page header
    create_page_header(
        title="Weapons",
        subtitle="Browse all weapons available on the Fibula server",
        icon=""
    )

    # Search and filter section
    col1, col2 = st.columns([3, 1])

    with col1:
        search_query = st.text_input(
            "Search weapons",
            placeholder="Search by name, type, monster, or NPC...",
            key="weapon_search"
        )

    with col2:
        # Get filter from navigation or button click
        default_filter = st.session_state.get("quick_filter", "All")
        nav_filter = st.session_state.get("weapon_filter", default_filter)
        selected_type = st.selectbox(
            "Filter by type",
            options=["All", "Sword", "Axe", "Club", "Distance", "Ammunition"],
            index=["All", "Sword", "Axe", "Club", "Distance", "Ammunition"].index(nav_filter) if nav_filter in ["All", "Sword", "Axe", "Club", "Distance", "Ammunition"] else 0,
            key="weapon_type_filter"
        )
        # Clear the session state filter
        if "weapon_filter" in st.session_state:
            del st.session_state["weapon_filter"]
    
    # Quick filter buttons
    st.markdown("**Quick Filters:**")
    col_btn1, col_btn2, col_btn3, col_btn4, col_btn5, col_btn6 = st.columns(6)
    
    with col_btn1:
        if st.button("All weapons", use_container_width=True, key="btn_all"):
            st.session_state.quick_filter = "All"
            st.rerun()
    
    with col_btn2:
        if st.button("Sword", use_container_width=True, key="btn_sword"):
            st.session_state.quick_filter = "Sword"
            st.rerun()
    
    with col_btn3:
        if st.button("Axe", use_container_width=True, key="btn_axe"):
            st.session_state.quick_filter = "Axe"
            st.rerun()
    
    with col_btn4:
        if st.button("Club", use_container_width=True, key="btn_club"):
            st.session_state.quick_filter = "Club"
            st.rerun()
    
    with col_btn5:
        if st.button("Distance", use_container_width=True, key="btn_distance"):
            st.session_state.quick_filter = "Distance"
            st.rerun()
    
    with col_btn6:
        if st.button("Ammunition", use_container_width=True, key="btn_ammo"):
            st.session_state.quick_filter = "Ammunition"
            st.rerun()
    
    # Use the filter from quick buttons if it was just set
    if "quick_filter" in st.session_state:
        selected_type = st.session_state.quick_filter

    # Load and filter weapons
    if search_query:
        weapons = search_weapons(search_query)
    else:
        weapons = load_weapons()

    # Apply type filter
    if selected_type != "All":
        weapons = [w for w in weapons if w.type.lower() == selected_type.lower()]

    if not weapons:
        st.info("No weapons found matching your criteria.")
        create_footer()
        return

    # Convert to DataFrame for display
    weapons_data = []
    for weapon in weapons:
        # Build image path from weapon data
        image_base64 = ""
        if weapon.image:
            # Convert relative path to absolute
            full_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                weapon.image.replace("./", "")
            )
            image_base64 = get_image_as_base64(full_path)
        
        # Handle sell_to - build tooltip data using NPCPrice objects
        sell_to_count = len(weapon.sell_to) if weapon.sell_to else 0
        sell_to_tooltip = ""
        if weapon.sell_to:
            # Group by price for cleaner display
            price_groups = {}
            for npc_price in weapon.sell_to:
                price = npc_price.price
                if price not in price_groups:
                    price_groups[price] = []
                npc_info = f"{npc_price.npc}"
                if npc_price.location:
                    npc_info += f" ({npc_price.location})"
                price_groups[price].append(npc_info)
            
            # Build tooltip with price groups
            for price in sorted(price_groups.keys(), reverse=True):
                sell_to_tooltip += f"Sell To ({price} gp)||"
                for npc_info in price_groups[price]:
                    sell_to_tooltip += f"{npc_info}||"
        
        # Handle dropped_by - can be strings or dicts
        dropped_by_list = []
        if weapon.dropped_by:
            for item in weapon.dropped_by:
                if isinstance(item, dict):
                    dropped_by_list.append(item.get('npc', str(item)))
                else:
                    dropped_by_list.append(str(item))
        dropped_by_text = ", ".join(dropped_by_list) if dropped_by_list else "-"
        
        # Handle reward_from - quest rewards
        reward_from_list = []
        if weapon.reward_from:
            for item in weapon.reward_from:
                if isinstance(item, dict):
                    reward_from_list.append(item.get('quest', str(item)))
                else:
                    reward_from_list.append(str(item))
        reward_from_text = ", ".join(reward_from_list) if reward_from_list else "-"
        
        weapons_data.append({
            "image_base64": image_base64,
            "Name": weapon.name,
            "Type": weapon.type.capitalize(),
            "Atk": weapon.attack,
            "Def": weapon.defense,
            "Weight": weapon.weight,
            "Hands": weapon.hands,
            "Sell To": sell_to_count,
            "sell_to_tooltip": sell_to_tooltip,
            "Looted from": dropped_by_text,
            "Reward from": reward_from_text
        })

    df = pd.DataFrame(weapons_data)

    # Custom CSS for table styling to match the screenshot
    st.markdown("""
        <style>
        .weapons-table-container {
            background-color: #1a1a1a;
            padding: 20px;
            border-radius: 4px;
            margin: 20px 0;
        }
        
        .weapons-table {
            width: 100%;
            border-collapse: collapse;
            background-color: #1a1a1a;
            font-size: 14px;
            color: #e0e0e0;
        }
        
        .weapons-table thead {
            background-color: #2d2d2d;
        }
        
        .weapons-table thead th {
            color: #e0e0e0;
            font-weight: bold;
            text-align: left;
            padding: 12px 8px;
            border-bottom: 2px solid #444;
            cursor: pointer;
            user-select: none;
            position: relative;
        }
        
        .weapons-table thead th:hover {
            background-color: #3d3d3d;
        }
        
        .weapons-table thead th.sortable::after {
            content: ' ⇅';
            opacity: 0.5;
            font-size: 11px;
            margin-left: 5px;
        }
        
        .weapons-table thead th.sorted-asc::after {
            content: ' ▲';
            opacity: 1;
        }
        
        .weapons-table thead th.sorted-desc::after {
            content: ' ▼';
            opacity: 1;
        }
        
        .weapons-table tbody tr:nth-child(odd) {
            background-color: #1a1a1a;
        }
        
        .weapons-table tbody tr:nth-child(even) {
            background-color: #2a2a2a;
        }
        
        .weapons-table tbody tr:hover {
            background-color: #353535 !important;
        }
        
        .weapons-table tbody td {
            padding: 10px 8px;
            border-bottom: 1px solid #333;
            color: #e0e0e0;
        }
        
        .weapons-table td.center,
        .weapons-table th.center {
            text-align: center;
        }
        
        /* Specific column widths */
        .weapons-table th:nth-child(3),
        .weapons-table td:nth-child(3) {
            width: 80px;
            max-width: 80px;
        }
        
        .weapons-table-container {
            display: block;
            margin: 0 auto;
            image-rendering: pixelated;
            image-rendering: -moz-crisp-edges;
            image-rendering: crisp-edges;
        }
        
        .table-info {
            color: #e0e0e0;
            margin-bottom: 10px;
            font-size: 14px;
        }
        
        /* Tooltip styling */
        .npc-count {
            cursor: help;
            position: relative;
            display: inline-block;
            color: #d4af37;
            font-weight: bold;
        }
        
        .npc-tooltip {
            visibility: hidden;
            position: absolute;
            z-index: 1000;
            background-color: #2d2d2d;
            color: #e0e0e0;
            border: 1px solid #444;
            border-radius: 4px;
            padding: 8px 12px;
            font-size: 13px;
            line-height: 1.6;
            min-width: 200px;
            max-width: 300px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            left: 50%;
            transform: translateX(-50%);
            bottom: 100%;
            margin-bottom: 8px;
            white-space: nowrap;
        }
        
        .npc-count:hover .npc-tooltip {
            visibility: visible;
        }
        
        .npc-tooltip-header {
            font-weight: bold;
            color: #ffcc00;
            margin-bottom: 4px;
            border-bottom: 1px solid #444;
            padding-bottom: 4px;
        }
        
        .npc-tooltip-item {
            margin: 2px 0;
            padding-left: 8px;
        }
        
        .npc-tooltip-item::before {
            content: '• ';
            color: #4da6ff;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Build HTML table
    table_html = '<div class="weapons-table-container">'
    table_html += f'<div class="table-info">Found {len(weapons)} weapon(s)</div>'
    table_html += '<table class="weapons-table" id="weaponsTable"><thead><tr>'
    table_html += '<th class="center sortable" data-column="0">Image</th>'
    table_html += '<th class="sortable" data-column="1">Name</th>'
    table_html += '<th class="center sortable" data-column="2">Type</th>'
    table_html += '<th class="center sortable" data-column="3">Atk</th>'
    table_html += '<th class="center sortable" data-column="4">Def</th>'
    table_html += '<th class="center sortable" data-column="5">Weight (oz.)</th>'
    table_html += '<th class="center sortable" data-column="6">Hands</th>'
    table_html += '<th class="center sortable" data-column="7">Sell To</th>'
    table_html += '<th class="sortable" data-column="8">Looted from</th>'
    table_html += '<th class="sortable" data-column="9">Reward from</th>'
    table_html += '</tr></thead><tbody>'
    
    for _, row in df.iterrows():
        table_html += '<tr>'
        # Image column
        if row["image_base64"]:
            table_html += f'<td class="center"><img src="{row["image_base64"]}" width="32" height="32" /></td>'
        else:
            table_html += '<td class="center">-</td>'
        # Other columns
        table_html += f'<td>{row["Name"]}</td>'
        table_html += f'<td class="center">{row["Type"]}</td>'
        table_html += f'<td class="center">{row["Atk"]}</td>'
        table_html += f'<td class="center">{row["Def"]}</td>'
        table_html += f'<td class="center">{row["Weight"]}</td>'
        table_html += f'<td class="center">{row["Hands"]}</td>'
        
        # Sell To column with tooltip
        if row["Sell To"] > 0:
            tooltip_lines = row["sell_to_tooltip"].split("||")
            tooltip_html = '<div class="npc-tooltip">'
            for i, line in enumerate(tooltip_lines):
                if line:
                    if "Sell To" in line:
                        tooltip_html += f'<div class="npc-tooltip-header">{line}</div>'
                    else:
                        tooltip_html += f'<div class="npc-tooltip-item">{line}</div>'
            tooltip_html += '</div>'
            table_html += f'<td class="center"><span class="npc-count">💰 {row["Sell To"]} NPCs{tooltip_html}</span></td>'
        else:
            table_html += '<td class="center">-</td>'
        
        # Looted from and Reward from columns
        table_html += f'<td>{row["Looted from"]}</td>'
        table_html += f'<td>{row["Reward from"]}</td>'
        
        table_html += '</tr>'
    
    table_html += '</tbody></table></div>'
    
    st.markdown(table_html, unsafe_allow_html=True)
    
    # Add sorting JavaScript using st.components
    st.components.v1.html("""
    <script>
    (function() {
        function sortTable() {
            const table = window.parent.document.querySelector('.weapons-table');
            if (!table) {
                setTimeout(sortTable, 100);
                return;
            }
            
            const headers = table.querySelectorAll('th.sortable');
            const sortDirections = {};
            
            headers.forEach((header, index) => {
                sortDirections[index] = true; // true = ascending
                
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
    main()
