"""
Fibulopedia - Main application entry point.

This is the main Streamlit application for Fibulopedia, an unofficial
guide and wiki for the Fibula Project (Tibia 7.1 OTS). The app provides
comprehensive information about weapons, equipment, spells, monsters,
quests, and server details.

To run the application:
    streamlit run app.py
"""

import streamlit as st
import json
from pathlib import Path
from datetime import datetime

from src.config import APP_TITLE, APP_SUBTITLE, APP_ICON
from src.ui.layout import (
    setup_page_config,
    load_custom_css,
    create_sidebar_navigation,
    create_footer
)
from src.logging_utils import setup_logger

# Initialize logger
logger = setup_logger(__name__)

def main() -> None:
    """Main function to render the home page."""
    logger.info("Rendering home page")
    
    # Welcome section with shortcuts inside
    st.markdown("""
        <style>
        .welcome-box {
            background: linear-gradient(135deg, rgba(30,30,30,0.95), rgba(40,40,40,0.95));
            border: 2px solid #d4af37;
            border-radius: 12px;
            padding: 2rem;
            margin: 2rem 0;
            text-align: center;
            box-shadow: 0 4px 20px rgba(212, 175, 55, 0.2);
            animation: fadeInUp 0.8s ease-out;
        }
        .welcome-box h1 {
            color: #d4af37;
            margin-bottom: 1rem;
            font-size: 2.5rem;
        }
        .welcome-box p {
            color: #cccccc;
            line-height: 1.8;
            margin-bottom: 0.5rem;
        }
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .shortcuts-title {
            color: #d4af37;
            font-size: 1.2rem;
            margin: 2rem 0 1rem 0;
            text-align: center;
        }
        </style>
        <div class="welcome-box">
            <h1>Welcome to Fibulopedia</h1>
            <p>Your comprehensive guide to the Fibula Project - a faithful recreation of the classic Tibia 7.1 experience.</p>
            <p>Explore weapons, equipment, spells, monsters, quests, and more.</p>
            <p><i>Please note that the website is currently under construction and may contain incomplete or sometimes even incorrect information. I try to ensure that all information is verified and confirmed, but if you notice any errors or omissions, please contact me on Discord.</i></p>
            <p>Molot (Grozze in-game)</p>    
        </div>
    """, unsafe_allow_html=True)
    
    # Shortcuts
    st.markdown('<p class="shortcuts-title"> Quick Access</p>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📊 Server Info", key="qa_server", use_container_width=True):
            st.switch_page("pages/Server_Info.py")
    with col2:
        if st.button("⚔️ Weapons", key="qa_weapons", use_container_width=True):
            st.session_state["weapon_filter"] = "All"
            st.switch_page("pages/Weapons.py")
    with col3:
        if st.button("🛡️ Equipment", key="qa_equipment", use_container_width=True):
            st.session_state["equipment_filter"] = "All"
            st.switch_page("pages/Equipment.py")
    with col4:
        if st.button("✨ Spells", key="qa_spells", use_container_width=True):
            st.switch_page("pages/Spells.py")
    
    st.markdown("---")
    
    # Main content area with news on left, search and links on right
    col_main, col_sidebar = st.columns([3, 1])
    
    with col_main:
        # Latest News in the main area
        st.markdown("## 📰 Latest News")
        
        # Load news from JSON
        news_file = Path("content/news.json")
        if news_file.exists():
            with open(news_file, "r", encoding="utf-8") as f:
                news_items = json.load(f)
            
            # Sort by date (newest first) and show max 5 items
            news_items = sorted(news_items, key=lambda x: x["date"], reverse=True)[:5]
            
            for news in news_items:
                # Category badge color
                category_colors = {
                    "announcement": "#4a90e2",
                    "update": "#50c878",
                    "info": "#ffd700",
                    "event": "#ff6347"
                }
                badge_color = category_colors.get(news.get("category", "info"), "#ffd700")
                
                st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, rgba(30,30,30,0.95), rgba(40,40,40,0.95));
                        border-left: 3px solid #d4af37;
                        border-radius: 8px;
                        padding: 1.5rem;
                        margin-bottom: 1.5rem;
                        transition: all 0.3s ease;
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                            <span style="
                                background: {badge_color};
                                color: white;
                                padding: 0.3rem 0.7rem;
                                border-radius: 4px;
                                font-size: 0.75rem;
                                text-transform: uppercase;
                                font-weight: bold;
                            ">{news.get('category', 'info')}</span>
                            <span style="color: #888; font-size: 0.9rem;">{news['date']}</span>
                        </div>
                        <h3 style="color: #d4af37; margin: 0.5rem 0; font-size: 1.4rem;">{news['title']}</h3>
                        <p style="color: #ccc; margin: 1rem 0 0 0; font-size: 1rem; line-height: 1.6;">{news['content']}</p>
                        <div style="color: #888; font-size: 0.85rem; margin-top: 0.75rem; font-style: italic;">
                            — {news.get('author', 'Admin')}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No news available yet.")
    
    with col_sidebar:
        # Quick Search at the top
        st.markdown("## 🔍 Quick Search")
        search_query = st.text_input(
            "Search",
            placeholder="Search for weapons, spells, monsters, quests...",
            label_visibility="collapsed"
        )
        
        if st.button("Search", type="primary", use_container_width=True):
            if search_query:
                st.session_state["search_query"] = search_query
                st.switch_page("pages/Search.py")
        
        st.markdown("---")
        
        # Quick Links section
        st.markdown("## 📌 Quick Links")
        st.markdown("""
            <div style="
                background: rgba(40,40,40,0.4);
                border: 2px dashed #555;
                border-radius: 8px;
                padding: 2rem;
                text-align: center;
                color: #888;
                min-height: 300px;
                display: flex;
                align-items: center;
                justify-content: center;
            ">
                <div>
                    <div style="font-size: 3rem; margin-bottom: 1rem;">📦</div>
                    <div style="font-size: 1rem;">Coming Soon</div>
                </div>
            </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    setup_page_config("Home", APP_ICON, layout="wide")
    load_custom_css()
    create_sidebar_navigation()
    
    main()
    
    create_footer()
