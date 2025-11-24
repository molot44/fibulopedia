"""
Spells page for Fibulopedia.

This page displays all spells with filtering by spell type (instant/rune), vocation and level.
Users can view spell incantations, mana costs, prices, and vocations.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import base64
import os

from src.services.spells_service import load_spells, search_spells, get_vocations, filter_spells_by_vocation
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

# Configure page
setup_page_config("Spells", "")
load_custom_css()
create_sidebar_navigation()


def main() -> None:
    """Main function to render the spells page."""
    logger.info("Rendering spells page")

    # Page header
    create_page_header(
        title="Spells",
        subtitle="Browse all spells available on the Fibula server",
        icon=""
    )

    # Search and filter section
    col1, col2 = st.columns([3, 1])

    with col1:
        search_query = st.text_input(
            "Search spells",
            placeholder="Search by name, incantation, vocation, or effect...",
            key="spell_search"
        )

    with col2:
        # Get filter from navigation or button click
        default_filter = st.session_state.get("quick_filter", "All")
        nav_filter = st.session_state.get("spell_filter", default_filter)
        selected_type = st.selectbox(
            "Filter by vocation",
            options=["All", "Sorcerer", "Druid", "Paladin", "Knight"],
            index=["All", "Sorcerer", "Druid", "Paladin", "Knight"].index(nav_filter) if nav_filter in ["All", "Sorcerer", "Druid", "Paladin", "Knight"] else 0,
            key="spell_vocation_filter"
        )
        # Clear the session state filter
        if "spell_filter" in st.session_state:
            del st.session_state["spell_filter"]
    
    # Quick filter buttons
    st.markdown("**Quick Filters:**")
    col_btn1, col_btn2, col_btn3, col_btn4, col_btn5 = st.columns(5)
    
    with col_btn1:
        if st.button("✨ All Vocations", use_container_width=True, key="btn_all"):
            st.session_state.quick_filter = "All"
            st.rerun()
    
    with col_btn2:
        if st.button("🔥 Sorcerer", use_container_width=True, key="btn_sorcerer"):
            st.session_state.quick_filter = "Sorcerer"
            st.rerun()
    
    with col_btn3:
        if st.button("🌿 Druid", use_container_width=True, key="btn_druid"):
            st.session_state.quick_filter = "Druid"
            st.rerun()
    
    with col_btn4:
        if st.button("🏹 Paladin", use_container_width=True, key="btn_paladin"):
            st.session_state.quick_filter = "Paladin"
            st.rerun()
    
    with col_btn5:
        if st.button("⚔️ Knight", use_container_width=True, key="btn_knight"):
            st.session_state.quick_filter = "Knight"
            st.rerun()
    
    # Use the filter from quick buttons if it was just set
    if "quick_filter" in st.session_state:
        selected_type = st.session_state.quick_filter

    # Load and filter spells
    if search_query:
        spells = search_spells(search_query)
    else:
        spells = load_spells()

    # Apply vocation filter
    if selected_type != "All":
        spells = [s for s in spells if selected_type in s.vocation or s.vocation == "All"]

    if not spells:
        st.info("No spells found matching your criteria.")
        create_footer()
        return

    # Group spells by (name, incantation) to merge duplicates for "All" view
    if selected_type == "All":
        spell_dict = {}
        for spell in spells:
            key = (spell.name, spell.incantation)
            if key in spell_dict:
                # Merge vocations
                existing_vocations = spell_dict[key]["vocations"]
                if spell.vocation not in existing_vocations:
                    spell_dict[key]["vocations"].append(spell.vocation)
            else:
                spell_dict[key] = {
                    "spell": spell,
                    "vocations": [spell.vocation]
                }
        
        # Convert back to list with merged vocations
        merged_spells = []
        for key, data in spell_dict.items():
            spell = data["spell"]
            spell.vocation = ", ".join(sorted(data["vocations"]))
            merged_spells.append(spell)
        spells = merged_spells

    # Convert to DataFrame for display
    spells_data = []
    for spell in spells:
        spell_type_display = "Instant" if spell.spell_type == "instant" else "Rune"
        premium_display = "Yes" if hasattr(spell, 'premium') and spell.premium else "No"
        
        # Magic Level To Use: show value only for runes
        magic_lvl_to_use = ""
        if hasattr(spell, 'magic_level_required') and spell.magic_level_required is not None:
            magic_lvl_to_use = spell.magic_level_required
        
        spells_data.append({
            "Magic_Level": spell.level,
            "Name": spell.name,
            "Type": spell_type_display,
            "Incantation": spell.incantation,
            "Mana": spell.mana,
            "Magic_Level_To_Use": magic_lvl_to_use,
            "Price": spell.price if hasattr(spell, 'price') else 0,
            "Premium": premium_display,
            "Vocation": spell.vocation
        })

    df = pd.DataFrame(spells_data)
    # Sort by Magic Level (character level) by default
    df = df.sort_values(by="Magic_Level", ascending=True)

    # Custom CSS for table styling
    st.markdown("""
        <style>
        .spells-table-container {
            background-color: #1a1a1a;
            padding: 20px;
            border-radius: 4px;
            margin: 20px 0;
        }
        
        .spells-table {
            width: 100%;
            border-collapse: collapse;
            background-color: #1a1a1a;
            font-size: 14px;
            color: #e0e0e0;
        }
        
        .spells-table thead {
            background-color: #2d2d2d;
        }
        
        .spells-table thead th {
            color: #e0e0e0;
            font-weight: bold;
            text-align: left;
            padding: 12px 8px;
            border-bottom: 2px solid #444;
            cursor: pointer;
            user-select: none;
            position: relative;
        }
        
        .spells-table thead th:hover {
            background-color: #3d3d3d;
        }
        
        .spells-table thead th.sortable::after {
            content: ' ⇅';
            opacity: 0.5;
            font-size: 11px;
            margin-left: 5px;
        }
        
        .spells-table thead th.sorted-asc::after {
            content: ' ▲';
            opacity: 1;
        }
        
        .spells-table thead th.sorted-desc::after {
            content: ' ▼';
            opacity: 1;
        }
        
        .spells-table tbody tr:nth-child(odd) {
            background-color: #1a1a1a;
        }
        
        .spells-table tbody tr:nth-child(even) {
            background-color: #2a2a2a;
        }
        
        .spells-table tbody tr:hover {
            background-color: #353535 !important;
        }
        
        .spells-table tbody td {
            padding: 10px 8px;
            border-bottom: 1px solid #333;
            color: #e0e0e0;
        }
        
        .spells-table td.center,
        .spells-table th.center {
            text-align: center;
        }
        
        /* Magic Level column width */
        .spells-table th:nth-child(1),
        .spells-table td:nth-child(1) {
            width: 60px;
            max-width: 60px;
        }
        
        .spells-table-container {
            display: block;
            margin: 0 auto;
        }
        
        .table-info {
            color: #e0e0e0;
            margin-bottom: 10px;
            font-size: 14px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Build HTML table
    table_html = '<div class="spells-table-container">'
    table_html += f'<div class="table-info">Found {len(spells)} spell(s)</div>'
    table_html += '<table class="spells-table" id="spellsTable"><thead><tr>'
    table_html += '<th class="center sortable" data-column="0">Magic Lvl</th>'
    table_html += '<th class="sortable" data-column="1">Name</th>'
    table_html += '<th class="center sortable" data-column="2">Type</th>'
    table_html += '<th class="sortable" data-column="3">Incantation</th>'
    table_html += '<th class="center sortable" data-column="4">Mana</th>'
    table_html += '<th class="center sortable" data-column="5">Magic Lvl To Use</th>'
    table_html += '<th class="center sortable" data-column="6">Price (gp)</th>'
    table_html += '<th class="center sortable" data-column="7">Premium</th>'
    table_html += '<th class="sortable" data-column="8">Vocations</th>'
    table_html += '</tr></thead><tbody>'
    
    for _, row in df.iterrows():
        table_html += '<tr>'
        table_html += f'<td class="center">{row["Magic_Level"]}</td>'
        table_html += f'<td>{row["Name"]}</td>'
        table_html += f'<td class="center">{row["Type"]}</td>'
        table_html += f'<td><em>{row["Incantation"]}</em></td>'
        table_html += f'<td class="center">{row["Mana"]}</td>'
        table_html += f'<td class="center">{row["Magic_Level_To_Use"]}</td>'
        table_html += f'<td class="center">{row["Price"]}</td>'
        table_html += f'<td class="center">{row["Premium"]}</td>'
        table_html += f'<td>{row["Vocation"]}</td>'
        table_html += '</tr>'
    
    table_html += '</tbody></table></div>'
    
    st.markdown(table_html, unsafe_allow_html=True)
    
    # Add sorting JavaScript
    st.components.v1.html("""
    <script>
    (function() {
        function sortTable() {
            const table = window.parent.document.querySelector('.spells-table');
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
