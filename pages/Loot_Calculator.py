"""
Loot Calculator page for Fibulopedia.

This calculator helps players determine the total value of their loot
and shows where they can sell each item.
"""

import streamlit as st
from typing import List, Dict, Optional
import base64
import os
import uuid
import streamlit_analytics2 as streamlit_analytics

from src.services.equipment_service import load_equipment
from src.services.weapons_service import load_weapons
from src.ui.layout import (
    setup_page_config,
    load_custom_css,
    create_page_header,
    create_sidebar_navigation,
    create_footer
)
from src.logging_utils import setup_logger
from src.analytics_utils import track_page_view

logger = setup_logger(__name__)

# Initialize session ID for analytics
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Start analytics tracking
streamlit_analytics.start_tracking()

# Configure page
setup_page_config("Loot Calculator", "")
load_custom_css()
create_sidebar_navigation("Loot Calculator")


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


def get_all_sellable_items():
    """Load all items that can be sold (have sell_to data)."""
    items = []
    
    # Load weapons
    weapons = load_weapons()
    for weapon in weapons:
        if weapon.sell_to and len(weapon.sell_to) > 0:
            # Get max price from all NPCs
            max_price = max(npc.price for npc in weapon.sell_to)
            items.append({
                "name": weapon.name,
                "type": "weapon",
                "category": weapon.type.capitalize(),
                "image": weapon.image,
                "sell_to": weapon.sell_to,
                "max_price": max_price,
                "id": weapon.id
            })
    
    # Load equipment
    equipment = load_equipment()
    for item in equipment:
        if item.sell_to and len(item.sell_to) > 0:
            max_price = max(npc.price for npc in item.sell_to)
            items.append({
                "name": item.name,
                "type": "equipment",
                "category": item.slot.capitalize(),
                "image": item.image,
                "sell_to": item.sell_to,
                "max_price": max_price,
                "id": item.id
            })
    
    # Sort by name
    items.sort(key=lambda x: x["name"])
    return items


def main() -> None:
    """Main function to render the loot calculator page."""
    logger.info("Rendering loot calculator page")
    
    # Track page view
    session_id = st.session_state.get("session_id")
    track_page_view("Loot Calculator", session_id)

    # Page header
    create_page_header(
        title="Loot Calculator",
        subtitle="Calculate the value of your loot and find the best places to sell",
        icon=""
    )

    # Initialize session state for loot list
    if "loot_list" not in st.session_state:
        st.session_state.loot_list = []

    # Load all sellable items
    all_items = get_all_sellable_items()
    
    if not all_items:
        st.warning("No sellable items found in the database.")
        return

    # Create item name to item mapping for quick lookup
    item_lookup = {item["name"]: item for item in all_items}
    item_names = [item["name"] for item in all_items]

    st.markdown("### Add Items to Your Loot")
    
    # Initialize last selected item tracker
    if "last_selected_item" not in st.session_state:
        st.session_state.last_selected_item = ""
    
    # Item selection
    col1, col2 = st.columns([4, 1])
    
    with col1:
        selected_item_name = st.selectbox(
            "Select item to add",
            options=[""] + item_names,
            index=0,
            help="Start typing to search for an item",
            key="item_selector"
        )
    
    with col2:
        st.markdown("<div style='margin-top: 0.25rem;'></div>", unsafe_allow_html=True)
        st.markdown("""
            <style>
            div[data-testid="stButton"] button[kind="secondary"]:has-text("🗑️ Clear All") {
                background: linear-gradient(135deg, rgba(244, 67, 54, 0.3), rgba(244, 67, 54, 0.2)) !important;
                border: 1px solid rgba(244, 67, 54, 0.5) !important;
                color: #f44336 !important;
            }
            div[data-testid="stButton"] button[kind="secondary"]:has-text("🗑️ Clear All"):hover {
                background: linear-gradient(135deg, rgba(244, 67, 54, 0.4), rgba(244, 67, 54, 0.3)) !important;
                border: 1px solid rgba(244, 67, 54, 0.7) !important;
            }
            </style>
        """, unsafe_allow_html=True)
        if st.button("🗑️ Clear All", use_container_width=True, help="Clear all items from loot list", type="secondary", key="clear_all_btn"):
            st.session_state.loot_list = []
            st.session_state.last_selected_item = ""
            # Force selectbox to reset by deleting its state
            if "item_selector" in st.session_state:
                del st.session_state.item_selector
            st.rerun()
    
    # Auto-add item when selected (only if it's a new selection)
    if selected_item_name and selected_item_name != "" and selected_item_name != st.session_state.last_selected_item:
        if selected_item_name in item_lookup:
            item_data = item_lookup[selected_item_name]
            # Check if item already exists in loot list
            existing_item = next((x for x in st.session_state.loot_list if x["name"] == selected_item_name), None)
            if not existing_item:
                st.session_state.loot_list.append({
                    "name": item_data["name"],
                    "type": item_data["type"],
                    "category": item_data["category"],
                    "image": item_data["image"],
                    "sell_to": item_data["sell_to"],
                    "max_price": item_data["max_price"],
                    "quantity": 1
                })
                st.session_state.last_selected_item = selected_item_name
                st.rerun()
            else:
                st.warning(f"⚠️ {selected_item_name} is already in your loot list. Adjust the quantity below.")
                st.session_state.last_selected_item = selected_item_name

    # Server log parser with custom styling
    st.markdown("""
        <style>
        div[data-testid="stExpander"] {
            background: linear-gradient(135deg, rgba(212,175,55,0.1), rgba(212,175,55,0.05));
            border: 1px solid rgba(212,175,55,0.3);
            border-radius: 8px;
        }
        div[data-testid="stExpander"] [data-testid="stExpanderHeader"] {
            color: #d4af37;
        }
        </style>
    """, unsafe_allow_html=True)
    
    with st.expander("📋 Or paste your Server Log to find items automatically"):
        st.markdown("Paste your server log below. The app will automatically extract all the items and add them to your loot list.")
        st.markdown("**Example format:**")
        st.code("13:58 You see a dwarven shield (Atk:0 Def:26).\nIt weighs 55.0 oz.")
        
        server_log = st.text_area(
            "Server Log",
            height=200,
            placeholder="Paste your server log here...",
            label_visibility="collapsed",
            key="server_log_input"
        )
        
        if st.button("🔍 Extract Items from Log", type="primary", use_container_width=True):
            if server_log:
                import re
                
                # Pattern to match "You see [a/an] ITEM_NAME (stats)"
                # Handles both "You see a plate armor" and "You see brass legs" (no article)
                pattern = r'You see (?:(?:a|an) )?([^(]+?)\s*\('
                matches = re.findall(pattern, server_log, re.IGNORECASE)
                
                if matches:
                    items_found = {}
                    items_not_found = []
                    
                    # Count occurrences and normalize names
                    for match in matches:
                        # Clean up the item name and capitalize first letter of each word
                        item_name = match.strip().title()
                        
                        # Try to find matching item in database (case-insensitive)
                        matched_item = None
                        for db_item_name in item_names:
                            if db_item_name.lower() == item_name.lower():
                                matched_item = db_item_name
                                break
                        
                        if matched_item:
                            items_found[matched_item] = items_found.get(matched_item, 0) + 1
                        else:
                            items_not_found.append(item_name)
                    
                    # Add found items to loot list
                    if items_found:
                        for item_name, count in items_found.items():
                            item_data = item_lookup[item_name]
                            # Check if item already exists in loot list
                            existing_item = next((x for x in st.session_state.loot_list if x["name"] == item_name), None)
                            if existing_item:
                                # Update quantity
                                existing_idx = st.session_state.loot_list.index(existing_item)
                                st.session_state.loot_list[existing_idx]["quantity"] += count
                            else:
                                # Add new item with count
                                st.session_state.loot_list.append({
                                    "name": item_data["name"],
                                    "type": item_data["type"],
                                    "category": item_data["category"],
                                    "image": item_data["image"],
                                    "sell_to": item_data["sell_to"],
                                    "max_price": item_data["max_price"],
                                    "quantity": count
                                })
                        
                        st.success(f"✅ Added {len(items_found)} item type(s) from server log!")
                        
                        # Show details
                        details = ", ".join([f"{name} x{count}" for name, count in items_found.items()])
                        st.info(f"📦 Items added: {details}")
                        
                        if items_not_found:
                            unique_not_found = list(set(items_not_found))
                            st.warning(f"⚠️ {len(unique_not_found)} item(s) not found in sellable database: {', '.join(unique_not_found[:10])}{'...' if len(unique_not_found) > 10 else ''}")
                            st.caption("💡 These items either don't exist in the database or don't have any NPCs that buy them.")
                        
                        st.rerun()
                    else:
                        st.error("❌ No matching items found in database. Make sure the items have sell prices configured.")
                else:
                    st.error("❌ No items found in the server log. Make sure it follows the correct format.")
            else:
                st.warning("Please paste your server log first.")

    st.markdown("---")

    # Display loot list
    if st.session_state.loot_list:
        st.markdown("### 📦 Your Loot")
        
        # Custom CSS for loot display
        st.markdown("""
            <style>
            .loot-item-card {
                background: linear-gradient(135deg, rgba(30,30,30,0.95), rgba(40,40,40,0.95));
                border: 2px solid #d4af37;
                border-radius: 8px;
                padding: 1rem;
                margin-bottom: 1rem;
            }
            .loot-item-header {
                display: flex;
                align-items: center;
                gap: 1rem;
                margin-bottom: 0.5rem;
            }
            .loot-item-image {
                image-rendering: pixelated;
                image-rendering: -moz-crisp-edges;
                image-rendering: crisp-edges;
            }
            .loot-item-name {
                color: #d4af37;
                font-size: 1.2rem;
                font-weight: bold;
            }
            .loot-item-category {
                color: #888;
                font-size: 0.9rem;
            }
            .loot-value {
                color: #50c878;
                font-size: 1.1rem;
                font-weight: bold;
            }
            .npc-sell-info {
                background: rgba(50,50,50,0.5);
                border-left: 3px solid #d4af37;
                padding: 0.5rem;
                margin-top: 0.5rem;
                border-radius: 4px;
                font-size: 0.9rem;
            }
            .total-value-box {
                background: linear-gradient(135deg, rgba(80,200,120,0.2), rgba(80,200,120,0.1));
                border: 3px solid #50c878;
                border-radius: 12px;
                padding: 1.5rem;
                text-align: center;
                margin-top: 2rem;
            }
            .total-value {
                font-size: 2rem;
                font-weight: bold;
                color: #50c878;
            }
            </style>
        """, unsafe_allow_html=True)
        
        total_value = 0
        items_to_remove = []
        all_npcs = {}  # Track all NPCs that buy items
        
        for idx, loot_item in enumerate(st.session_state.loot_list):
            # Create columns for each loot item
            col_img, col_info, col_qty, col_value, col_remove, col_npcs = st.columns([1, 3, 2, 2, 1, 4])
            
            with col_img:
                if loot_item["image"]:
                    image_b64 = get_image_as_base64(loot_item["image"])
                    if image_b64:
                        st.markdown(f'<img src="{image_b64}" width="48" class="loot-item-image">', unsafe_allow_html=True)
            
            with col_info:
                st.markdown(f"**{loot_item['name']}**")
                st.markdown(f"<span style='color: #888; font-size: 0.85rem;'>{loot_item['category']}</span>", unsafe_allow_html=True)
            
            with col_qty:
                new_qty = st.number_input(
                    "Quantity",
                    min_value=1,
                    max_value=10000,
                    value=loot_item["quantity"],
                    step=1,
                    key=f"qty_{idx}",
                    label_visibility="collapsed"
                )
                if new_qty != loot_item["quantity"]:
                    st.session_state.loot_list[idx]["quantity"] = new_qty
                    st.rerun()
            
            with col_value:
                item_value = loot_item["max_price"] * loot_item["quantity"]
                total_value += item_value
                st.markdown(f"<div class='loot-value'>{item_value:,} gp</div>", unsafe_allow_html=True)
                st.markdown(f"<span style='color: #888; font-size: 0.75rem;'>{loot_item['max_price']} gp each</span>", unsafe_allow_html=True)
            
            with col_remove:
                if st.button("🗑️", key=f"remove_{idx}", help="Remove item"):
                    items_to_remove.append(idx)
            
            with col_npcs:
                # Show NPC sell info inline with better formatting
                # Group by price and location
                npc_list = []
                for npc in loot_item["sell_to"]:
                    npc_list.append({
                        "name": npc.npc,
                        "location": npc.location,
                        "price": npc.price
                    })
                
                # Sort by price (highest first)
                npc_list.sort(key=lambda x: x["price"], reverse=True)
                
                # Display as pills with location
                npc_html = "<div style='display: flex; flex-wrap: wrap; gap: 4px; align-items: center;'>"
                for npc_data in npc_list:
                    location_text = f" ({npc_data['location']})" if npc_data['location'] else ""
                    npc_html += f"""<span style='display: inline-block; background: linear-gradient(135deg, rgba(212,175,55,0.2), rgba(212,175,55,0.1)); border: 1px solid #d4af37; border-radius: 12px; padding: 4px 10px; font-size: 0.75rem; color: #e0e0e0; white-space: nowrap; margin: 2px 0;'><span style='color: #d4af37; font-weight: bold;'>{npc_data['name']}</span><span style='color: #e0e0e0;'>{location_text}</span> <span style='color: #50c878; margin-left: 4px;'>{npc_data['price']} gp</span></span>"""
                npc_html += "</div>"
                st.markdown(npc_html, unsafe_allow_html=True)
            
            # Track only NPCs with best prices for this item
            max_price = max(npc.price for npc in loot_item["sell_to"])
            for npc in loot_item["sell_to"]:
                if npc.price == max_price:  # Only track NPCs offering the best price
                    npc_key = f"{npc.npc} ({npc.location})"
                    if npc_key not in all_npcs:
                        all_npcs[npc_key] = []
                    all_npcs[npc_key].append({
                        "name": loot_item["name"],
                        "price": npc.price,
                        "quantity": loot_item["quantity"],
                        "total": npc.price * loot_item["quantity"]
                    })
        
        # Remove items marked for deletion
        for idx in reversed(items_to_remove):
            st.session_state.loot_list.pop(idx)
        if items_to_remove:
            st.rerun()
        
        # Total value display
        st.markdown(f"""
            <div class="total-value-box">
                <div style="font-size: 1.2rem; color: #e0e0e0; margin-bottom: 0.5rem;">Total Loot Value</div>
                <div class="total-value">{total_value:,} gp</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Best Selling Route - Always visible, clean and fast
        if all_npcs:
            st.markdown("### Best Selling Route")
            
            # Calculate totals per NPC
            npc_totals = {npc: sum(item["total"] for item in items) for npc, items in all_npcs.items()}
            sorted_npcs = sorted(all_npcs.items(), key=lambda x: npc_totals[x[0]], reverse=True)
            
            # Display as clean compact table
            for npc_key, items in sorted_npcs:
                npc_total = sum(item["total"] for item in items)
                
                # Extract NPC name and location
                npc_name = npc_key.split(" (")[0]
                npc_location = npc_key.split(" (")[1].rstrip(")")
                
                # Build items list
                items_text = ", ".join([f"{item['name']} (x{item['quantity']})" for item in items])
                
                # Create compact card
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, rgba(212,175,55,0.15), rgba(212,175,55,0.05)); 
                                border-left: 3px solid #d4af37;
                                border-radius: 4px; 
                                padding: 8px 12px; 
                                margin-bottom: 8px;'>
                        <div style='display: flex; justify-content: space-between; align-items: flex-start; gap: 12px;'>
                            <div style='flex: 1;'>
                                <div style='margin-bottom: 4px;'>
                                    <span style='color: #d4af37; font-weight: bold; font-size: 1rem;'>{npc_name}</span>
                                    <span style='color: #888; margin-left: 6px; font-size: 0.85rem;'>📍 {npc_location}</span>
                                </div>
                                <div style='color: #aaa; font-size: 0.85rem;'>{items_text}</div>
                            </div>
                            <div style='color: #50c878; font-weight: bold; font-size: 1.1rem; white-space: nowrap;'>{npc_total:,} gp</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    
    else:
        st.info("Add items to your loot list to calculate their value and see where you can sell them.")

    # Footer
    create_footer()


if __name__ == "__main__":
    try:
        main()
    finally:
        # Stop analytics tracking
        streamlit_analytics.stop_tracking()
