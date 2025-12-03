"""
Tools page for Fibulopedia.

This page displays all tools available in the game.
Users can view tool stats, search by name, and see where to obtain them.
"""

import streamlit as st
import pandas as pd
import base64
import os
import html

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
                ext = os.path.splitext(image_path)[1][1:]
                return f"data:image/{ext};base64,{encoded}"
    except Exception as e:
        logger.error(f"Error loading image {image_path}: {e}")
    return ""


def load_tools():
    """Load tools from JSON file."""
    import json
    try:
        with open('./content/tools.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading tools: {e}")
        return []


# Configure page
setup_page_config("Tools", "")
load_custom_css()
create_sidebar_navigation("Tools")


def main() -> None:
    """Main function to render the tools page."""
    logger.info("Rendering tools page")
    
    # Page header
    create_page_header(
        title="Tools",
        subtitle="Browse all tools available on the Fibula server",
        icon=""
    )
    
    # Search section
    search_query = st.text_input(
        "Search tools",
        placeholder="Search by name or description...",
        key="tools_search"
    )
    
    # Load tools
    tools = load_tools()
    
    # Apply search filter
    if search_query:
        search_lower = search_query.lower()
        tools = [
            t for t in tools
            if search_lower in t.get('name', '').lower() or
               search_lower in t.get('description', '').lower()
        ]
    
    if not tools:
        st.info("No tools found matching your criteria.")
        create_footer()
        return
    
    # Build DataFrame for display
    data = []
    for tool in tools:
        # Get image
        image_path = tool.get('image', '')
        image_base64 = get_image_as_base64(image_path) if image_path else ""
        
        data.append({
            'image_base64': image_base64,
            'Name': tool.get('name', 'Unknown'),
            'Weight': tool.get('weight', 0),
            'Description': tool.get('description', '')
        })
    
    df = pd.DataFrame(data)
    
    # Add CSS styling
    st.markdown("""
        <style>
        .tools-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
            background-color: #1e1e1e;
            color: #e0e0e0;
        }
        
        .tools-table th {
            background-color: #2d2d2d;
            color: #ffcc00;
            padding: 12px 8px;
            text-align: left;
            font-weight: bold;
            border-bottom: 2px solid #444;
            position: sticky;
            top: 0;
            z-index: 10;
        }
        
        .tools-table td {
            padding: 10px 8px;
            border-bottom: 1px solid #333;
        }
        
        .tools-table tr:hover {
            background-color: #252525;
        }
        
        .tools-table th.sortable {
            cursor: pointer;
            user-select: none;
        }
        
        .tools-table th.sortable:hover {
            background-color: #3d3d3d;
        }
        
        .tools-table th.sortable::after {
            content: ' ⇅';
            opacity: 0.3;
        }
        
        .tools-table th.sorted-asc::after {
            content: ' ↑';
            opacity: 1;
        }
        
        .tools-table th.sorted-desc::after {
            content: ' ↓';
            opacity: 1;
        }
        
        .tools-table .center {
            text-align: center;
        }
        
        .tools-table img {
            vertical-align: middle;
            image-rendering: pixelated;
            image-rendering: -moz-crisp-edges;
            image-rendering: crisp-edges;
        }
        
        .tools-table td:last-child {
            max-width: 400px;
            word-wrap: break-word;
        }
        
        .tools-table-container {
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
            position: relative;
            cursor: help;
            color: #4da6ff;
            text-decoration: underline dotted;
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
    table_html = '<div class="tools-table-container">'
    table_html += f'<div class="table-info">Found {len(tools)} tool(s)</div>'
    table_html += '<table class="tools-table" id="toolsTable"><thead><tr>'
    table_html += '<th class="center sortable" data-column="0">Image</th>'
    table_html += '<th class="sortable" data-column="1">Name</th>'
    table_html += '<th class="center sortable" data-column="2">Weight (oz.)</th>'
    table_html += '<th class="sortable" data-column="3">Description</th>'
    table_html += '</tr></thead><tbody>'
    
    for _, row in df.iterrows():
        table_html += '<tr>'
        # Image column
        if row["image_base64"]:
            table_html += f'<td class="center"><img src="{row["image_base64"]}" width="32" height="32" /></td>'
        else:
            table_html += '<td class="center">-</td>'
        # Name
        table_html += f'<td>{row["Name"]}</td>'
        # Weight
        table_html += f'<td class="center">{row["Weight"]}</td>'
        # Description column
        table_html += f'<td>{row["Description"]}</td>'
        
        table_html += '</tr>'
    
    table_html += '</tbody></table></div>'
    
    st.markdown(table_html, unsafe_allow_html=True)
    
    # Add sorting JavaScript
    st.components.v1.html("""
    <script>
    (function() {
        function sortTable() {
            const table = window.parent.document.querySelector('.tools-table');
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
    
    create_footer()


if __name__ == "__main__":
    main()
