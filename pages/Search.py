"""
Search page for Fibulopedia.

This page provides global search functionality across all content types:
weapons, equipment, spells, monsters, and quests.
"""

import streamlit as st

from src.services.search_service import search_all, search_by_entity_type
from src.ui.layout import (
    setup_page_config,
    load_custom_css,
    create_page_header,
    create_sidebar_navigation,
    create_footer
)
from src.ui.components import create_search_result_item
from src.logging_utils import setup_logger

logger = setup_logger(__name__)

# Configure page
setup_page_config("Search", "🔍")
load_custom_css()
create_sidebar_navigation("Search")


def main() -> None:
    """Main function to render the search page."""
    logger.info("Rendering search page")
    
    # Page header
    create_page_header(
        title="Advanced Search",
        subtitle="Search across all content: weapons, equipment, spells, monsters, and quests",
        icon="🔍"
    )
    
    # Check if there's a query from the home page
    initial_query = st.session_state.get("search_query", "")
    
    # Search input
    col1, col2, col3 = st.columns([4, 1, 1])
    
    with col1:
        search_query = st.text_input(
            "Search query",
            value=initial_query,
            placeholder="Enter your search terms...",
            key="global_search_input"
        )
    
    with col2:
        entity_filter = st.selectbox(
            "Content type",
            options=["All", "Weapon", "Equipment", "Spell", "Monster", "Quest"],
            key="entity_type_filter"
        )
    
    with col3:
        search_button = st.button("Search", type="primary", use_container_width=True)
    
    # Clear the session state query after using it
    if "search_query" in st.session_state:
        del st.session_state["search_query"]
    
    # Perform search
    if search_query and (search_button or initial_query):
        with st.spinner("Searching..."):
            if entity_filter == "All":
                results = search_all(search_query)
            else:
                results = search_by_entity_type(search_query, entity_filter.lower())
        
        # Display results
        st.markdown("---")
        st.subheader(f"Search Results for: '{search_query}'")
        st.markdown(f"**Found {len(results)} result(s)**")
        
        if not results:
            st.info("No results found. Try different search terms or check your spelling.")
        else:
            # Group results by entity type
            entity_types = {}
            for result in results:
                if result.entity_type not in entity_types:
                    entity_types[result.entity_type] = []
                entity_types[result.entity_type].append(result)
            
            # Display results grouped by type
            for entity_type, type_results in entity_types.items():
                with st.expander(f"{entity_type.title()} ({len(type_results)})", expanded=True):
                    for result in type_results:
                        create_search_result_item(
                            entity_type=result.entity_type,
                            name=result.name,
                            snippet=result.snippet,
                            entity_id=result.entity_id
                        )
                        st.markdown("<br>", unsafe_allow_html=True)
    else:
        # Show search tips
        st.markdown("---")
        st.subheader("Search Tips")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **How to search effectively:**
            - Use specific keywords (e.g., "dragon", "fire spell", "steel")
            - Search by monster names to find loot
            - Search by NPC names to find items
            - Use the content type filter to narrow results
            """)
        
        with col2:
            st.markdown("""
            **Search examples:**
            - `"sword"` - Find all swords
            - `"thais"` - Find quests and monsters in Thais
            - `"healing"` - Find healing spells
            - `"dragon"` - Find dragons and dragon-related items
            """)
        
        st.markdown("---")
        st.subheader("Quick Links")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("⚔️ Browse Weapons", use_container_width=True):
                st.switch_page("pages/2_Weapons.py")
        
        with col2:
            if st.button("🛡️ Browse Equipment", use_container_width=True):
                st.switch_page("pages/3_Equipment.py")
        
        with col3:
            if st.button("✨ Browse Spells", use_container_width=True):
                st.switch_page("pages/4_Spells.py")
        
        with col4:
            if st.button("👹 Browse Monsters", use_container_width=True):
                st.switch_page("pages/5_Monsters.py")
    
    # Footer
    create_footer()


if __name__ == "__main__":
    main()
