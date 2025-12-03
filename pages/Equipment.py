"""
Equipment page for Fibulopedia.

This page displays all equipment organized by slots (helmet, armor, legs, boots, etc).
Users can view equipment stats, search by name or slot, and see where to obtain them.
"""

import streamlit as st
import pandas as pd
import base64
import os

from src.services.equipment_service import load_equipment, search_equipment, get_equipment_slots
from src.ui.layout import (
    setup_page_config,
    load_custom_css,
    create_page_header,
    create_sidebar_navigation,
    create_footer
)
from src.ui.components import create_type_badge
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
setup_page_config("Equipment", "🛡️")
load_custom_css()
create_sidebar_navigation("Equipment")


def main() -> None:
    """Main function to render the equipment page."""
    logger.info("Rendering equipment page")
    
    # Page header
    create_page_header(
        title="Equipment",
        subtitle="Browse all equipment available on the Fibula server",
        icon=""
    )
    
    # Search and filter section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "Search equipment",
            placeholder="Search by name, slot, monster, or NPC...",
            key="equipment_search"
        )
    
    with col2:
        # Get filter from navigation or button click
        default_filter = st.session_state.get("quick_filter_equip", "Helmets")
        nav_filter = st.session_state.get("equipment_filter", default_filter)
        selected_slot = st.selectbox(
            "Filter by slot",
            options=["Helmets", "Armor", "Legs", "Boots", "Shields", "Amulets & Rings"],
            index=["Helmets", "Armor", "Legs", "Boots", "Shields", "Amulets & Rings"].index(nav_filter) if nav_filter in ["Helmets", "Armor", "Legs", "Boots", "Shields", "Amulets & Rings"] else 0,
            key="equipment_slot_filter"
        )
        # Clear the session state filter
        if "equipment_filter" in st.session_state:
            del st.session_state["equipment_filter"]
    
    # Quick filter buttons
    st.markdown("**Quick Filters:**")
    col_btn0, col_btn1, col_btn2, col_btn3, col_btn4, col_btn5, col_btn6 = st.columns(7)
    
    with col_btn0:
        if st.button("All Equipment", use_container_width=True, key="btn_all_equip"):
            st.session_state.quick_filter_equip = None
            st.rerun()
    
    with col_btn1:
        if st.button("Helmets", use_container_width=True, key="btn_helmets"):
            st.session_state.quick_filter_equip = "Helmets"
            st.rerun()
    
    with col_btn2:
        if st.button("Armor", use_container_width=True, key="btn_armor"):
            st.session_state.quick_filter_equip = "Armor"
            st.rerun()
    
    with col_btn3:
        if st.button("Legs", use_container_width=True, key="btn_legs"):
            st.session_state.quick_filter_equip = "Legs"
            st.rerun()
    
    with col_btn4:
        if st.button("Boots", use_container_width=True, key="btn_boots"):
            st.session_state.quick_filter_equip = "Boots"
            st.rerun()
    
    with col_btn5:
        if st.button("Shields", use_container_width=True, key="btn_shields"):
            st.session_state.quick_filter_equip = "Shields"
            st.rerun()
    
    with col_btn6:
        if st.button("Amulets & Rings", use_container_width=True, key="btn_amulets"):
            st.session_state.quick_filter_equip = "Amulets & Rings"
            st.rerun()
    
    # Use the filter from quick buttons if it was just set
    if "quick_filter_equip" in st.session_state:
        selected_slot = st.session_state.quick_filter_equip
    
    # Load and filter equipment
    if search_query:
        equipment = search_equipment(search_query)
    else:
        equipment = load_equipment()
    
    # Apply slot filter (only if not None/All Equipment)
    if selected_slot:
        # Map display names to actual slot names in JSON
        slot_mapping = {
            "Helmets": "helmet",
            "Armor": "armor",
            "Legs": "legs",
            "Boots": "boots",
            "Shields": "shields",
            "Amulets & Rings": ["amulet", "ring"]
        }
        
        target_slots = slot_mapping.get(selected_slot, selected_slot.lower())
        
        if isinstance(target_slots, list):
            equipment = [e for e in equipment if e.slot.lower() in target_slots]
        else:
            equipment = [e for e in equipment if e.slot.lower() == target_slots]
    
    # Determine if we're showing rings/amulets (properties) or defense equipment
    is_accessories = selected_slot == "Amulets & Rings"
    
    if not equipment:
        st.info("No equipment found matching your criteria.")
        create_footer()
        return
    
    # Convert to DataFrame for display
    equipment_data = []
    for item in equipment:
        # Build image path from equipment data
        image_base64 = ""
        if hasattr(item, 'image') and item.image:
            # Convert relative path to absolute
            full_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                item.image.replace("./", "")
            )
            image_base64 = get_image_as_base64(full_path)
        
        # Handle dropped_by
        dropped_by_list = []
        if item.dropped_by:
            for drop_item in item.dropped_by:
                if isinstance(drop_item, dict):
                    dropped_by_list.append(drop_item.get('npc', str(drop_item)))
                else:
                    dropped_by_list.append(str(drop_item))
        dropped_by_text = ", ".join(dropped_by_list) if dropped_by_list else "-"
        
        # Handle reward_from
        reward_from_list = []
        if hasattr(item, 'reward_from') and item.reward_from:
            for reward_item in item.reward_from:
                if isinstance(reward_item, dict):
                    reward_from_list.append(reward_item.get('quest', str(reward_item)))
                else:
                    reward_from_list.append(str(reward_item))
        reward_from_text = ", ".join(reward_from_list) if reward_from_list else "-"
        
        # Build data row - include both defense and properties
        row_data = {
            "image_base64": image_base64,
            "Name": item.name,
            "Slot": item.slot.capitalize(),
            "Def": item.defense,
            "Properties": getattr(item, 'properties', None) or "-",
            "Weight": item.weight,
            "Dropped by": dropped_by_text,
            "Reward from": reward_from_text
        }
        
        equipment_data.append(row_data)
    
    df = pd.DataFrame(equipment_data)
    
    # Custom CSS for table styling
    st.markdown("""
        <style>
        .equipment-table-container {
            background-color: #1a1a1a;
            padding: 20px;
            border-radius: 4px;
            margin: 20px 0;
        }
        
        .equipment-table {
            width: 100%;
            border-collapse: collapse;
            background-color: #1a1a1a;
            font-size: 14px;
            color: #e0e0e0;
        }
        
        .equipment-table thead {
            background-color: #2d2d2d;
        }
        
        .equipment-table thead th {
            color: #e0e0e0;
            font-weight: bold;
            text-align: left;
            padding: 12px 8px;
            border-bottom: 2px solid #444;
            cursor: pointer;
            user-select: none;
            position: relative;
        }
        
        .equipment-table thead th:hover {
            background-color: #3d3d3d;
        }
        
        .equipment-table thead th.sortable::after {
            content: ' ⇅';
            opacity: 0.5;
            font-size: 11px;
            margin-left: 5px;
        }
        
        .equipment-table thead th.sorted-asc::after {
            content: ' ▲';
            opacity: 1;
        }
        
        .equipment-table thead th.sorted-desc::after {
            content: ' ▼';
            opacity: 1;
        }
        
        .equipment-table tbody tr:nth-child(odd) {
            background-color: #1a1a1a;
        }
        
        .equipment-table tbody tr:nth-child(even) {
            background-color: #2a2a2a;
        }
        
        .equipment-table tbody tr:hover {
            background-color: #353535 !important;
        }
        
        .equipment-table tbody td {
            padding: 10px 8px;
            border-bottom: 1px solid #333;
            color: #e0e0e0;
        }
        
        .equipment-table td.center,
        .equipment-table th.center {
            text-align: center;
        }
        
        /* Specific column widths */
        .equipment-table th:nth-child(3),
        .equipment-table td:nth-child(3) {
            width: 80px;
            max-width: 80px;
        }
        
        .equipment-table-container {
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
        </style>
    """, unsafe_allow_html=True)
    
    # Build HTML table
    table_html = '<div class="equipment-table-container">'
    table_html += f'<div class="table-info">Found {len(equipment)} equipment item(s)</div>'
    table_html += '<table class="equipment-table" id="equipmentTable"><thead><tr>'
    table_html += '<th class="center sortable" data-column="0">Image</th>'
    table_html += '<th class="sortable" data-column="1">Name</th>'
    table_html += '<th class="center sortable" data-column="2">Slot</th>'
    
    # Dynamic column: Armor or Effect
    if is_accessories:
        table_html += '<th class="sortable" data-column="3">Effect</th>'
    else:
        table_html += '<th class="center sortable" data-column="3">Armor</th>'
    
    table_html += '<th class="center sortable" data-column="4">Weight (oz.)</th>'
    table_html += '<th class="sortable" data-column="5">Looted from</th>'
    table_html += '<th class="sortable" data-column="6">Reward from</th>'
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
        table_html += f'<td class="center">{row["Slot"]}</td>'
        
        # Dynamic column content
        if is_accessories:
            table_html += f'<td>{row["Properties"]}</td>'
        else:
            table_html += f'<td class="center">{row["Def"]}</td>'
        
        table_html += f'<td class="center">{row["Weight"]}</td>'
        table_html += f'<td>{row["Dropped by"]}</td>'
        table_html += f'<td>{row["Reward from"]}</td>'
        table_html += '</tr>'
    
    table_html += '</tbody></table></div>'
    
    st.markdown(table_html, unsafe_allow_html=True)
    
    # Add sorting JavaScript
    st.components.v1.html("""
    <script>
    (function() {
        function sortTable() {
            const table = window.parent.document.querySelector('.equipment-table');
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


