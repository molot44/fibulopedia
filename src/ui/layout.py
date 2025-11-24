"""
Layout utilities for Fibulopedia.

This module provides functions for creating consistent page layouts,
headers, footers, and structural elements across all pages.
"""

import streamlit as st
from pathlib import Path
from typing import Optional

from src.config import (
    APP_TITLE,
    APP_SUBTITLE,
    ASSETS_DIR,
    LOGO_PATH,
    NAVIGATION_ITEMS,
    STYLES_PATH,
    Theme
)


@st.cache_data
def load_icon_path(icon_name: str) -> str:
    """Cache icon paths to avoid repeated file system checks."""
    icon_path = ASSETS_DIR / "items" / icon_name
    return str(icon_path) if icon_path.exists() else None


def load_custom_css() -> None:
    """
    Load and apply custom CSS styles from the assets folder.
    
    This function should be called once at the beginning of each page
    to ensure consistent styling throughout the application.
    
    Example:
        >>> load_custom_css()
    """
    # Try to load CSS from file
    if STYLES_PATH.exists():
        with open(STYLES_PATH, "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    else:
        # Fallback to inline CSS if file doesn\'\'t exist
        st.markdown(
            f"""
            <style>
            /* Base styles */
            .main {{
                background-color: {Theme.BACKGROUND_COLOR};
                color: {Theme.TEXT_COLOR};
                font-family: {Theme.FONT_FAMILY};
            }}
            
            /* Hub cards */
            .hub-card {{
                background-color: {Theme.SURFACE_COLOR};
                padding: {Theme.CARD_PADDING};
                border-radius: {Theme.CARD_BORDER_RADIUS};
                border: 2px solid {Theme.PRIMARY_COLOR};
                margin-bottom: 1rem;
                text-align: center;
                transition: transform 0.2s;
            }}
            
            .hub-card:hover {{
                transform: translateY(-5px);
                border-color: {Theme.SECONDARY_COLOR};
            }}
            
            .hub-card-icon {{
                font-size: 3rem;
                margin-bottom: 0.5rem;
            }}
            
            .hub-card-title {{
                color: {Theme.PRIMARY_COLOR};
                font-family: {Theme.HEADING_FONT};
                margin-bottom: 0.5rem;
            }}
            
            .hub-card-description {{
                color: {Theme.TEXT_MUTED};
                font-size: 0.9rem;
            }}
            
            /* Regular cards */
            .card {{
                background-color: {Theme.SURFACE_COLOR};
                padding: {Theme.CARD_PADDING};
                border-radius: {Theme.CARD_BORDER_RADIUS};
                border-left: 4px solid {Theme.PRIMARY_COLOR};
                margin-bottom: 1rem;
            }}
            
            /* Badges */
            .stat-badge {{
                display: inline-block;
                padding: 0.25rem 0.75rem;
                margin: 0.25rem;
                border-radius: 4px;
                color: {Theme.BACKGROUND_COLOR};
                font-size: 0.85rem;
            }}
            
            .type-badge {{
                display: inline-block;
                padding: 0.2rem 0.6rem;
                margin: 0.2rem;
                border-radius: 4px;
                color: white;
                font-size: 0.75rem;
                font-weight: bold;
                text-transform: uppercase;
            }}
            
            /* Search results */
            .search-result-item {{
                background-color: {Theme.SURFACE_COLOR};
                padding: 1rem;
                border-radius: {Theme.CARD_BORDER_RADIUS};
                border-left: 3px solid {Theme.PRIMARY_COLOR};
                margin-bottom: 0.75rem;
            }}
            
            .search-result-header {{
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin-bottom: 0.5rem;
            }}
            
            .search-result-icon {{
                font-size: 1.5rem;
            }}
            
            .search-result-name {{
                color: {Theme.PRIMARY_COLOR};
                font-size: 1.1rem;
            }}
            
            .search-result-snippet {{
                color: {Theme.TEXT_MUTED};
                font-size: 0.9rem;
                margin: 0;
            }}
            
            /* Headings */
            h1, h2, h3 {{
                color: {Theme.PRIMARY_COLOR};
                font-family: {Theme.HEADING_FONT};
            }}
            
            /* Links */
            a {{
                color: {Theme.PRIMARY_COLOR};
                text-decoration: none;
            }}
            
            a:hover {{
                color: {Theme.SECONDARY_COLOR};
                text-decoration: underline;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )


def setup_page_config(page_title: str, page_icon: str = "", layout: str = "wide") -> None:
    """
    Configure the Streamlit page settings.
    
    Args:
        page_title: Title of the page (shown in browser tab).
        page_icon: Emoji icon for the page.
        layout: Page layout ("wide" or "centered").
    
    Example:
        >>> setup_page_config("Weapons", "")
    """
    st.set_page_config(
        page_title=f"{page_title} - {APP_TITLE}",
        page_icon=page_icon,
        layout=layout,
        initial_sidebar_state="expanded"
    )


def create_page_header(title: str, subtitle: Optional[str] = None, icon: str = "") -> None:
    """
    Create a consistent page header with title and optional subtitle.
    
    Args:
        title: Main page title.
        subtitle: Optional subtitle or description.
        icon: Optional emoji icon.
    
    Example:
        >>> create_page_header("Weapons", "Browse all available weapons", "")
    """
    st.title(f"{icon} {title}")
    if subtitle:
        st.markdown(f"*{subtitle}*")
    
    st.markdown("---")


def create_sidebar_navigation() -> None:
    """
    Create a sidebar with navigation links to all main pages.
    
    This function should be called on each page to provide consistent
    navigation throughout the application.
    
    Example:
        >>> create_sidebar_navigation()
    """
    with st.sidebar:
        # Display logo at the top with effects
        if LOGO_PATH.exists():
            import base64
            with open(LOGO_PATH, "rb") as f:
                logo_data = base64.b64encode(f.read()).decode()
            
            st.markdown(f"""
                <style>
                .logo-container {{ 
                    text-align: center; 
                    padding: 0px 0 10px 0; 
                    animation: fadeIn 1s ease-in;
                }}
                .logo-container img {{ 
                    filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.6));
                    transition: all 0.3s ease;
                    max-width: 100%;
                    height: auto;
                }}
                .logo-container img:hover {{ 
                    transform: scale(1.08);
                    filter: drop-shadow(0 0 20px rgba(212, 175, 55, 0.9));
                }}
                .subtitle-text {{ 
                    text-align: center; 
                    color: #aaa; 
                    font-size: 0.85rem; 
                    font-style: italic; 
                    margin: 15px 0 10px 0; 
                    padding: 0 10px; 
                    line-height: 1.4; 
                    animation: fadeIn 1.2s ease-in;
                }}
                @keyframes fadeIn {{ 
                    from {{ opacity: 0; transform: translateY(-10px); }} 
                    to {{ opacity: 1; transform: translateY(0); }} 
                }}
                .gold-separator {{ 
                    height: 2px; 
                    background: linear-gradient(to right, transparent, #d4af37, transparent); 
                    margin: 15px 0; 
                    box-shadow: 0 0 5px rgba(212, 175, 55, 0.5);
                }}
                </style>
                <div class="logo-container">
                    <img src="data:image/png;base64,{logo_data}" alt="Fibulopedia Logo">
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="gold-separator"></div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle-text">Community guide and wiki for Fibula Project<br>a classic Tibia style OTS</div>', unsafe_allow_html=True)
        st.markdown('<div class="gold-separator"></div>', unsafe_allow_html=True)
        
        # Navigation section
        st.subheader("Navigation")
        if st.button(" Home", key="nav_Home", use_container_width=True):
            st.switch_page("app.py")
        
        # Server Info button with icon
        serverinfo_icon_path = load_icon_path("Parchment_of_Interest.gif")
        if serverinfo_icon_path:
            col1, col2 = st.columns([1, 5])
            with col1:
                st.image(serverinfo_icon_path, width=32)
            with col2:
                if st.button("Server Info", key="nav_Server_Info", use_container_width=True):
                    st.switch_page("pages/Server_Info.py")
        else:
            if st.button(" Server Info", key="nav_Server_Info_fallback", use_container_width=True):
                st.switch_page("pages/Server_Info.py")
        # Tibia Map button with icon
        map_icon_path = load_icon_path("Compass.gif")
        if map_icon_path:
            col1, col2 = st.columns([1, 5])
            with col1:
                st.image(map_icon_path, width=32)
            with col2:
                if st.button("Tibia Map", key="nav_Map", use_container_width=True):
                    st.switch_page("pages/Map.py")
        else:
            if st.button(" Tibia Map", key="nav_Map_fallback", use_container_width=True):
                st.switch_page("pages/Map.py")
        
        # Gear section
        st.subheader("Gear")
        
        # Weapons with dropdown - using toggle with icon
        if "show_weapons" not in st.session_state:
            st.session_state.show_weapons = False
        
        # Load weapons icon
        weapons_icon_path = ASSETS_DIR / "items" / "magic_sword.gif"
        if weapons_icon_path.exists():
            # Użyj kolumn dla ikony i przycisku
            col1, col2 = st.columns([1, 5])
            with col1:
                st.image(str(weapons_icon_path), width=32)
            with col2:
                if st.button("Weapons", key="nav_weapons_toggle", use_container_width=True):
                    st.session_state.show_weapons = not st.session_state.show_weapons
                    st.rerun()
        else:
            if st.button(" Weapons", key="nav_weapons_toggle_fallback", use_container_width=True):
                st.session_state.show_weapons = not st.session_state.show_weapons
                st.rerun()
        
        if st.session_state.show_weapons:
            with st.container(border=True):
                weapon_categories = ["All", "Sword", "Axe", "Club", "Distance", "Ammunition"]
                for category in weapon_categories:
                    if st.button(f" {category}", key=f"nav_weapon_{category}", use_container_width=True, type="secondary"):
                        st.session_state["weapon_filter"] = category
                        st.session_state.show_weapons = False
                        st.switch_page("pages/Weapons.py")
        
        # Equipment with dropdown - using toggle with icon
        if "show_equipment" not in st.session_state:
            st.session_state.show_equipment = False
        
        # Load equipment icon
        equipment_icon_path = load_icon_path("magic_plate_armor.gif")
        if equipment_icon_path:
            col1, col2 = st.columns([1, 5])
            with col1:
                st.image(equipment_icon_path, width=32)
            with col2:
                if st.button("Equipment", key="nav_equipment_toggle", use_container_width=True):
                    st.session_state.show_equipment = not st.session_state.show_equipment
        else:
            if st.button(" Equipment", key="nav_equipment_toggle_fallback", use_container_width=True):
                st.session_state.show_equipment = not st.session_state.show_equipment
        
        if st.session_state.show_equipment:
            with st.container(border=True):
                equipment_categories = ["All", "Helmets", "Armor", "Legs", "Shields", "Amulets & Rings"]
                for category in equipment_categories:
                    if st.button(f" {category}", key=f"nav_equipment_{category}", use_container_width=True, type="secondary"):
                        st.session_state["equipment_filter"] = category
                        st.session_state.show_equipment = False
                        st.switch_page("pages/Equipment.py")
        
        # Tools button with icon
        tools_icon_path = load_icon_path("rope.gif")
        if tools_icon_path:
            col1, col2 = st.columns([1, 5])
            with col1:
                st.image(tools_icon_path, width=32)
            with col2:
                if st.button("Tools", key="nav_Tools", use_container_width=True):
                    st.switch_page("pages/Tools.py")
        else:
            if st.button("Tools", key="nav_Tools_fallback", use_container_width=True):
                st.switch_page("pages/Tools.py")
        
        # Others section
        st.subheader("Others")
        
        # Spells button (direct navigation with icon)
        spells_icon_path = load_icon_path("purpletome.gif")
        if spells_icon_path:
            col1, col2 = st.columns([1, 5])
            with col1:
                st.image(spells_icon_path, width=32)
            with col2:
                if st.button("Spells", key="nav_Spells", use_container_width=True):
                    st.switch_page("pages/Spells.py")
        else:
            if st.button("Spells", key="nav_Spells_fallback", use_container_width=True):
                st.switch_page("pages/Spells.py")
        
        # Monsters button with icon
        monsters_icon_path = load_icon_path("demon.gif")
        if monsters_icon_path:
            col1, col2 = st.columns([1, 5])
            with col1:
                st.image(monsters_icon_path, width=32)
            with col2:
                if st.button("Monsters", key="nav_Monsters", use_container_width=True):
                    st.switch_page("pages/Monsters.py")
        else:
            if st.button(" Monsters", key="nav_Monsters_fallback", use_container_width=True):
                st.switch_page("pages/Monsters.py")
        # Quests button with icon
        quests_icon_path = load_icon_path("chest.gif")
        if quests_icon_path:
            col1, col2 = st.columns([1, 5])
            with col1:
                st.image(quests_icon_path, width=32)
            with col2:
                if st.button("Quests", key="nav_Quests", use_container_width=True):
                    st.switch_page("pages/Quests.py")
        else:
            if st.button(" Quests", key="nav_Quests_fallback", use_container_width=True):
                st.switch_page("pages/Quests.py")
        
        # Search button (outside categories)
        st.markdown("---")
        if st.button(" Search", key="nav_Search", use_container_width=True):
            st.switch_page("pages/Search.py")
        
        # HIDDEN: Item Editor (admin tool) - temporarily disabled for public release
        # st.markdown("---")
        # st.caption("Admin Tools")
        # if st.button("✏️ Item Editor", key="nav_Item_Editor", use_container_width=True):
        #     st.switch_page("pages/Item_Editor.py")


def create_footer() -> None:
    """
    Create a consistent footer for all pages.
    
    Example:
        >>> create_footer()
    """
    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align: center; color: {Theme.TEXT_MUTED}; padding: 1rem;">
            <p>{APP_TITLE} - An unofficial guide for Fibula Project</p>
            <p style="font-size: 0.8rem;">
                Tibia is a registered trademark of CipSoft GmbH. 
                This is a fan-made project and is not affiliated with CipSoft.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def create_hub_grid(cards: list[dict[str, str]], columns: int = 3) -> None:
    """
    Create a grid layout of hub cards.
    
    Args:
        cards: List of card dictionaries with title, icon, description, and page.
        columns: Number of columns in the grid.
    
    Example:
        >>> cards = [
        ...     {"title": "Weapons", "icon": "", "description": "...", "page": "Weapons"}
        ... ]
        >>> create_hub_grid(cards, columns=3)
    """
    # Create rows of cards
    for i in range(0, len(cards), columns):
        cols = st.columns(columns)
        for j, col in enumerate(cols):
            if i + j < len(cards):
                card = cards[i + j]
                with col:
                    from src.ui.components import create_hub_card
                    create_hub_card(
                        title=card["title"],
                        icon=card["icon"],
                        description=card["description"],
                        page=card["page"]
                    )


def create_search_bar(placeholder: str = "Search...", key: str = "search") -> Optional[str]:
    """
    Create a search input bar.
    
    Args:
        placeholder: Placeholder text for the search input.
        key: Unique key for the search input.
    
    Returns:
        The search query string, or None if empty.
    
    Example:
        >>> query = create_search_bar("Search weapons...")
        >>> if query:
        ...     results = search_weapons(query)
    """
    query = st.text_input(
        "Search",
        placeholder=placeholder,
        key=key,
        label_visibility="collapsed"
    )
    
    return query.strip() if query else None

