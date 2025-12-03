"""
Server Info page for Fibulopedia.

This page displays server information including rates, version,
rules, and links to the community.
"""

import streamlit as st

from src.services.server_info_service import load_server_info
from src.services.fibula_status import fetch_online_count
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
setup_page_config("Server Info", "ℹ")
load_custom_css()
create_sidebar_navigation("Server Info")


@st.cache_data(ttl=60)
def get_cached_online_count():
    """Fetch online player count with 60-second cache."""
    return fetch_online_count()


def main() -> None:
    """Main function to render the server info page."""
    logger.info("Rendering server info page")

    # Page header
    create_page_header(
        title="Server Information",
        subtitle="Learn about Fibula Project rates and features",
        icon="ℹ"
    )
    
    # Note: Online player count feature disabled due to Cloudflare protection
    # on the MyAAC website preventing automated scraping
    
    st.markdown("---")

    # Load server info
    server_info = load_server_info()

    if not server_info:
        st.error("Unable to load server information. Please check the configuration.")
        create_footer()
        return

    # Server overview
    st.markdown(f"## {server_info.name}")
    st.markdown(server_info.description)
    
    # Additional info about Fibula Project
    if server_info.additional_info:
        st.markdown("")
        st.markdown(server_info.additional_info)

    st.markdown("---")

    # Server rates and features in two columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Server Rates")
        
        if server_info.rates:
            rate_col1, rate_col2, rate_col3, rate_col4 = st.columns(4)
            
            with rate_col1:
                exp_rate = server_info.rates.get("exp", 1)
                st.metric(label="EXP Rate", value=f"{exp_rate}x")
            
            with rate_col2:
                loot_rate = server_info.rates.get("loot", 1)
                st.metric(label="Loot Rate", value=f"{loot_rate}x")
            
            with rate_col3:
                skill_rate = server_info.rates.get("skill", 1)
                st.metric(label="Skill Rate", value=f"{skill_rate}x")
            
            with rate_col4:
                magic_rate = server_info.rates.get("magic", 1)
                st.metric(label="Magic Rate", value=f"{magic_rate}x")

    with col2:
        st.subheader("Server Features")
        st.markdown("""
        - Classic Tibia 7.1 experience
        - No level or vocation requirements for equipment
        - Authentic monster spawns and loot
        - Original quest system
        - Classic map layout
        - Active player base
        - Discord community
        - Regular events
        """)

    st.markdown("---")

    # Technical information and Community Links in two columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Technical Information")
        st.markdown(f"**Client Version:** {server_info.version}")
        st.markdown(f"**Server Type:** Open Tibia Server (OTS)")
        st.markdown(f"**Style:** Classic Tibia 7.1")

    with col2:
        st.markdown('<h3 style="color: #d4af37;"> Community Links</h3>', unsafe_allow_html=True)
        
        if server_info.website:
            st.markdown(f"[ Official Website]({server_info.website})")

        if server_info.discord:
            st.markdown(f"[ Discord Server]({server_info.discord})")

        st.markdown("[ Fibulopedia Home](../)")

    # Footer
    create_footer()


if __name__ == "__main__":
    main()
