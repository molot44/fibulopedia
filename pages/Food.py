"""
Food page for Fibulopedia.

This page displays all food items with sortable tables and filtering options.
Users can view food stats including HP gains and efficiency ratings.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import base64

from src.services.food_service import load_food, search_food
from src.ui.layout import (
    setup_page_config,
    load_custom_css,
    create_page_header,
    create_sidebar_navigation,
    create_footer
)
from src.config import PROJECT_ROOT
from src.logging_utils import setup_logger

logger = setup_logger(__name__)


def get_image_as_base64(image_path: Path) -> str:
    """Convert an image file to base64 string."""
    try:
        if image_path.exists():
            with open(image_path, "rb") as f:
                data = f.read()
                encoded = base64.b64encode(data).decode()
                ext = image_path.suffix[1:]  # Get extension without dot
                return f"data:image/{ext};base64,{encoded}"
    except Exception as e:
        logger.error(f"Error loading image {image_path}: {e}")
    return ""

# Configure page
setup_page_config("Food", "🍖")
load_custom_css()
create_sidebar_navigation()


def main() -> None:
    """Main function to render the food page."""
    logger.info("Rendering food page")

    # Page header
    create_page_header(
        title="Food",
        subtitle="Browse all food items available on the Fibula server",
        icon=""
    )

    # Search section
    search_query = st.text_input(
        "Search food items",
        placeholder="Search by name...",
        key="food_search"
    )

    # Load and filter food
    if search_query:
        food_items = search_food(search_query)
    else:
        food_items = load_food()

    if not food_items:
        st.info("No food items found matching your criteria.")
        create_footer()
        return

    # Convert to DataFrame for display
    food_data = []
    for food in food_items:
        # Build image path from food data
        image_base64 = ""
        if food.image:
            # Convert relative path to absolute using PROJECT_ROOT
            image_path = PROJECT_ROOT / food.image.replace("./", "")
            image_base64 = get_image_as_base64(image_path)
        
        food_data.append({
            "image_base64": image_base64,
            "Name": food.name,
            "HP Gain": food.hp_gain if food.hp_gain is not None else "?",
            "Weight": food.weight if food.weight is not None else "?",
            "HP Gain per Oz.": food.hp_per_oz if food.hp_per_oz is not None else "?",
            "HP Gain per GP": food.hp_per_gp if food.hp_per_gp is not None else "?"
        })

    df = pd.DataFrame(food_data)
    
    # Sort by HP Gain per GP (descending) - handle "?" values (put them at the end)
    df['sort_key'] = df['HP Gain per GP'].apply(lambda x: -999999 if x == "?" else float(x) if x != "?" else -999999)
    df = df.sort_values('sort_key', ascending=False)
    df = df.drop('sort_key', axis=1)

    # Custom CSS for table styling
    st.markdown("""
        <style>
        .food-table-container {
            background-color: #1a1a1a;
            padding: 20px;
            border-radius: 4px;
            margin: 20px 0;
        }
        
        .food-table {
            width: 100%;
            border-collapse: collapse;
            background-color: #1a1a1a;
            font-size: 14px;
            color: #e0e0e0;
        }
        
        .food-table thead {
            background-color: #2d2d2d;
        }
        
        .food-table thead th {
            color: #e0e0e0;
            font-weight: bold;
            text-align: left;
            padding: 12px 8px;
            border-bottom: 2px solid #444;
            cursor: pointer;
            user-select: none;
            position: relative;
        }
        
        .food-table thead th.sortable:hover {
            background-color: #3d3d3d;
        }
        
        .food-table thead th.center {
            text-align: center;
        }
        
        .food-table thead th.sorted-asc::after {
            content: ' ▲';
            font-size: 10px;
        }
        
        .food-table thead th.sorted-desc::after {
            content: ' ▼';
            font-size: 10px;
        }
        
        .food-table tbody tr {
            border-bottom: 1px solid #333;
        }
        
        .food-table tbody tr:hover {
            background-color: #2a2a2a;
        }
        
        .food-table tbody td {
            padding: 10px 8px;
            vertical-align: middle;
        }
        
        .food-table tbody td.center {
            text-align: center;
        }
        
        .table-info {
            color: #999;
            font-size: 13px;
            margin-bottom: 10px;
            font-style: italic;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Build HTML table
    table_html = '<div class="food-table-container">'
    table_html += f'<div class="table-info">Found {len(food_items)} food item(s)</div>'
    table_html += '<table class="food-table" id="foodTable"><thead><tr>'
    table_html += '<th class="center sortable" data-column="0">Image</th>'
    table_html += '<th class="sortable" data-column="1">Name</th>'
    table_html += '<th class="center sortable" data-column="2">HP Gain</th>'
    table_html += '<th class="center sortable" data-column="3">Weight (Oz.)</th>'
    table_html += '<th class="center sortable" data-column="4">HP Gain per Oz.</th>'
    table_html += '<th class="center sortable" data-column="5">HP Gain per GP</th>'
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
        table_html += f'<td class="center">{row["HP Gain"]}</td>'
        table_html += f'<td class="center">{row["Weight"]}</td>'
        table_html += f'<td class="center">{row["HP Gain per Oz."]}</td>'
        table_html += f'<td class="center">{row["HP Gain per GP"]}</td>'
        table_html += '</tr>'
    
    table_html += '</tbody></table></div>'
    
    st.markdown(table_html, unsafe_allow_html=True)
    
    # Add sorting JavaScript
    st.components.v1.html("""
    <script>
    (function() {
        function sortTable() {
            const table = window.parent.document.querySelector('.food-table');
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
                        
                        // Handle special values
                        if (aValue === '-') aValue = '0';
                        if (bValue === '-') bValue = '0';
                        if (aValue === '?') aValue = '999999';
                        if (bValue === '?') bValue = '999999';
                        
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
