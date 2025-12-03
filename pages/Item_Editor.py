"""
Item Editor page for Fibulopedia.

This page allows easy editing of buy_from and sell_to data for items.
"""

import streamlit as st
import json
import os
from typing import Dict, List, Any

from src.ui.layout import (
    setup_page_config,
    load_custom_css,
    create_page_header,
    create_sidebar_navigation,
    create_footer
)
from src.logging_utils import setup_logger

logger = setup_logger(__name__)

# Configure page
setup_page_config("Item Editor", "✏️")
load_custom_css()
create_sidebar_navigation("Item Editor")

# Available NPCs and locations
NPCS = [
    "Hardek", "Memech", "Ulrik", "Romella", "Rowenna", "Shanar", 
    "Willard", "Uzgod", "Robert", "Baltim", "Brengus", "Cedrik",
    "Esrik", "Flint", "Gamel", "Habdel", "Morpel", "Sam", "Turvy"
]

LOCATIONS = [
    "Thais", "Ankrahmun", "Greenshore", "Venore", "Carlin", "Ab'Dendriel",
    "Edron", "Kazordoon", "Svargrond", "Tyrsung", "Port Hope", "Liberty Bay",
    "Farmine", "Rathleton", "Darashia", "Yalahar", "Bounac", "Gray Beach"
]


def load_json_file(filepath: str) -> List[Dict[str, Any]]:
    """Load items from JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading {filepath}: {e}")
        return []


def save_json_file(filepath: str, data: List[Dict[str, Any]]) -> bool:
    """Save items to JSON file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Error saving {filepath}: {e}")
        return False


def get_item_by_id(items: List[Dict], item_id: str) -> Dict:
    """Find item by ID."""
    for item in items:
        if item.get('id') == item_id:
            return item
    return {}


def main() -> None:
    """Main function to render the item editor page."""
    logger.info("Rendering item editor page")
    
    # Page header
    create_page_header(
        title="Item Editor",
        subtitle="Edit NPC trading data for weapons, equipment, and tools",
        icon="✏️"
    )
    
    # File selection
    col1, col2 = st.columns(2)
    with col1:
        file_type = st.radio(
            "Select file to edit:",
            ["Weapons", "Equipment", "Tools"],
            horizontal=True
        )
    
    if file_type == "Weapons":
        filepath = "./content/weapons.json"
    elif file_type == "Equipment":
        filepath = "./content/equipment.json"
    else:  # Tools
        filepath = "./content/tools.json"
    
    # Load items
    items = load_json_file(filepath)
    
    if not items:
        st.error(f"Could not load {file_type.lower()} data!")
        create_footer()
        return
    
    # Create item list for selection
    item_names = [f"{item.get('name', 'Unknown')} ({item.get('id', '')})" for item in items]
    
    with col2:
        selected_name = st.selectbox(
            "Select item to edit:",
            options=item_names,
            key="item_selector"
        )
    
    # Get selected item ID
    selected_id = selected_name.split('(')[1].strip(')')
    selected_item = get_item_by_id(items, selected_id)
    
    if not selected_item:
        st.error("Item not found!")
        create_footer()
        return
    
    st.markdown("---")
    
    # Display item info
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.markdown(f"**Name:** {selected_item.get('name', 'N/A')}")
    with col_info2:
        st.markdown(f"**Type:** {selected_item.get('type', 'N/A').title()}")
    with col_info3:
        st.markdown(f"**ID:** {selected_item.get('id', 'N/A')}")
    
    st.markdown("---")
    
    # Edit sections
    col_buy, col_sell = st.columns(2)
    
    # BUY FROM section
    with col_buy:
        st.subheader("🛒 Buy From")
        
        # Initialize buy_from in session state
        if 'buy_from_data' not in st.session_state or st.session_state.get('current_item_id') != selected_id:
            st.session_state.buy_from_data = selected_item.get('buy_from', []).copy()
            st.session_state.current_item_id = selected_id
        
        # Display existing entries
        if st.session_state.buy_from_data:
            for idx, entry in enumerate(st.session_state.buy_from_data):
                col_a, col_b, col_c, col_d = st.columns([3, 3, 2, 1])
                with col_a:
                    st.text_input(f"NPC", value=entry.get('npc', ''), key=f"buy_npc_{idx}", disabled=True)
                with col_b:
                    st.text_input(f"Location", value=entry.get('location', ''), key=f"buy_loc_{idx}", disabled=True)
                with col_c:
                    st.number_input(f"Price", value=entry.get('price', 0), key=f"buy_price_{idx}", disabled=True)
                with col_d:
                    if st.button("🗑️", key=f"buy_del_{idx}", help="Delete"):
                        st.session_state.buy_from_data.pop(idx)
                        st.rerun()
        else:
            st.info("No buy data yet")
        
        # Add new entry
        st.markdown("**Add New:**")
        col_new1, col_new2, col_new3, col_new4 = st.columns([3, 3, 2, 1])
        with col_new1:
            new_buy_npc = st.selectbox("NPC", options=[""] + NPCS, key="new_buy_npc")
        with col_new2:
            new_buy_loc = st.selectbox("Location", options=[""] + LOCATIONS, key="new_buy_loc")
        with col_new3:
            new_buy_price = st.number_input("Price", min_value=0, value=0, key="new_buy_price")
        with col_new4:
            if st.button("➕", key="add_buy", help="Add"):
                if new_buy_npc and new_buy_loc:
                    st.session_state.buy_from_data.append({
                        "npc": new_buy_npc,
                        "location": new_buy_loc,
                        "price": new_buy_price
                    })
                    st.rerun()
    
    # SELL TO section
    with col_sell:
        st.subheader("💰 Sell To")
        
        # Initialize sell_to in session state
        if 'sell_to_data' not in st.session_state or st.session_state.get('current_item_id') != selected_id:
            st.session_state.sell_to_data = selected_item.get('sell_to', []).copy()
        
        # Display existing entries
        if st.session_state.sell_to_data:
            for idx, entry in enumerate(st.session_state.sell_to_data):
                col_a, col_b, col_c, col_d = st.columns([3, 3, 2, 1])
                with col_a:
                    st.text_input(f"NPC", value=entry.get('npc', ''), key=f"sell_npc_{idx}", disabled=True)
                with col_b:
                    st.text_input(f"Location", value=entry.get('location', ''), key=f"sell_loc_{idx}", disabled=True)
                with col_c:
                    st.number_input(f"Price", value=entry.get('price', 0), key=f"sell_price_{idx}", disabled=True)
                with col_d:
                    if st.button("🗑️", key=f"sell_del_{idx}", help="Delete"):
                        st.session_state.sell_to_data.pop(idx)
                        st.rerun()
        else:
            st.info("No sell data yet")
        
        # Add new entry
        st.markdown("**Add New:**")
        col_new1, col_new2, col_new3, col_new4 = st.columns([3, 3, 2, 1])
        with col_new1:
            new_sell_npc = st.selectbox("NPC", options=[""] + NPCS, key="new_sell_npc")
        with col_new2:
            new_sell_loc = st.selectbox("Location", options=[""] + LOCATIONS, key="new_sell_loc")
        with col_new3:
            new_sell_price = st.number_input("Price", min_value=0, value=0, key="new_sell_price")
        with col_new4:
            if st.button("➕", key="add_sell", help="Add"):
                if new_sell_npc and new_sell_loc:
                    st.session_state.sell_to_data.append({
                        "npc": new_sell_npc,
                        "location": new_sell_loc,
                        "price": new_sell_price
                    })
                    st.rerun()
    
    st.markdown("---")
    
    # Save button
    col_save1, col_save2, col_save3 = st.columns([1, 1, 1])
    with col_save2:
        if st.button("💾 Save Changes", type="primary", use_container_width=True):
            # Update item with new data
            selected_item['buy_from'] = st.session_state.buy_from_data
            selected_item['sell_to'] = st.session_state.sell_to_data
            
            # Find and update item in list
            for idx, item in enumerate(items):
                if item.get('id') == selected_id:
                    items[idx] = selected_item
                    break
            
            # Save to file
            if save_json_file(filepath, items):
                st.success(f"✅ Successfully saved changes to {selected_item.get('name', 'item')}!")
                # Clear session state for next edit
                if 'buy_from_data' in st.session_state:
                    del st.session_state.buy_from_data
                if 'sell_to_data' in st.session_state:
                    del st.session_state.sell_to_data
                st.rerun()
            else:
                st.error("❌ Failed to save changes!")
    
    create_footer()


if __name__ == "__main__":
    main()
