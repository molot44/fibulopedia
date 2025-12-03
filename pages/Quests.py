"""
Quests page for Fibulopedia.

This page displays all available quests with their locations and rewards.
Future versions will include step-by-step walkthroughs.
"""

import streamlit as st

from src.ui.layout import (
    setup_page_config,
    load_custom_css,
    create_page_header,
    create_sidebar_navigation,
    create_footer
)

# Configure page
setup_page_config("Quests", "📜")
load_custom_css()
create_sidebar_navigation("Quests")

# Page header
create_page_header(
    title="Quests",
    subtitle="Quest information coming soon",
    icon=""
)

# Work in progress message
st.markdown("""
    <div style="
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, rgba(30,30,30,0.95), rgba(40,40,40,0.95));
        border: 2px solid #d4af37;
        border-radius: 12px;
        margin: 2rem 0;
    ">
        <h2 style="color: #d4af37; font-size: 2.5rem; margin-bottom: 1rem;">🚧 Work in Progress 🚧</h2>
        <p style="color: #cccccc; font-size: 1.2rem;">This page is currently under construction.</p>
        <p style="color: #888; font-size: 1rem; margin-top: 1rem;">Check back soon for quest guides and information!</p>
    </div>
""", unsafe_allow_html=True)

# Footer
create_footer()
