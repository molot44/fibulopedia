"""
Search page for Fibulopedia.

This page provides global search functionality across all content types:
weapons, equipment, spells, monsters, and quests.
"""

import streamlit as st
import uuid
import streamlit_analytics2 as streamlit_analytics

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
from src.analytics_utils import track_page_view
from src.services.search_service import get_page_route

logger = setup_logger(__name__)

# Check for form submissions FIRST and convert to navigation
for key in list(st.session_state.keys()):
    if key.startswith("FormSubmitter:nav_") and key.endswith("-View →"):
        if st.session_state[key]:
            # Extract entity info from form key: FormSubmitter:nav_weapon_axe_001_123456-View →
            parts = key.replace("FormSubmitter:nav_", "").replace("-View →", "").split("_")
            if len(parts) >= 3:
                entity_type = parts[0]
                page_route = get_page_route(entity_type)
                logger.info(f"✓✓✓ Form submitted: {key} -> navigating to {page_route}")
                st.switch_page(page_route)

# Check for pending navigation
logger.info(f">>> Session state keys: {list(st.session_state.keys())}")
if "navigate_to" in st.session_state:
    logger.info(f">>> navigate_to value: {st.session_state['navigate_to']}")
    if st.session_state["navigate_to"]:
        page = st.session_state["navigate_to"]
        st.session_state["navigate_to"] = None  # Clear immediately
        logger.info(f"✓✓✓ NAVIGATING TO: {page}")
        st.switch_page(page)
else:
    logger.info(">>> navigate_to NOT in session_state")

# Initialize session ID for analytics
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Start analytics tracking
streamlit_analytics.start_tracking()

# Configure page
setup_page_config("Search", "🔍")
load_custom_css()
create_sidebar_navigation("Search")


def main() -> None:
    """Main function to render the search page."""
    
    # Track page view
    track_page_view("Search", st.session_state.session_id)
    
    logger.info("Rendering search page")
    
    # Page header
    create_page_header(
        title="Advanced Search",
        subtitle="Search across all content: weapons, equipment, spells, monsters, and quests",
        icon=""
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
            options=["All", "Weapon", "Equipment", "Spell", "Monster", "Quest", "Food", "Tool"],
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
                st.markdown(f"### {entity_type.title()} ({len(type_results)})")
                for result in type_results:
                    create_search_result_item(
                        entity_type=result.entity_type,
                        name=result.name,
                        snippet=result.snippet,
                        entity_id=result.entity_id,
                        page_route=result.page_route,
                        image_base64=result.image_base64
                    )
                    st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("---")
    
    # Footer
    create_footer()


if __name__ == "__main__":
    try:
        main()
    finally:
        streamlit_analytics.stop_tracking()
