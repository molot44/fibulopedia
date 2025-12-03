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
from src.services.fibula_status import fetch_online_count
import base64

# Initialize logger
logger = setup_logger(__name__)


@st.cache_data(ttl=60)
def get_cached_online_count():
    """Fetch online player count with 60-second cache."""
    return fetch_online_count()


def main() -> None:
    """Main function to render the home page."""
    logger.info("Rendering home page")
    
    # Large centered logo with subtitle and rotworm gif
    logo_path = Path("assets/logo_fibulopedia.png")
    rotworm_path = Path("assets/monsters/rotworm.gif")
    
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            logo_data = base64.b64encode(f.read()).decode()
        
        rotworm_data = ""
        if rotworm_path.exists():
            with open(rotworm_path, "rb") as f:
                rotworm_data = base64.b64encode(f.read()).decode()
        
        st.markdown(f"""
            <style>
                .main-logo-container {{
                    text-align: center;
                    margin: -3rem 0 0.5rem 0;
                    padding-top: 0;
                    animation: fadeInDown 1s ease-out;
                    position: relative;
                }}
                .main-logo-container img.logo {{
                    max-width: 450px;
                    width: 100%;
                    height: auto;
                    filter: drop-shadow(0 0 20px rgba(212, 175, 55, 0.4));
                    transition: transform 0.3s ease, filter 0.3s ease;
                }}
                .main-logo-container img.logo:hover {{
                    transform: scale(1.02);
                    filter: drop-shadow(0 0 30px rgba(212, 175, 55, 0.6));
                }}
                .rotworm-gif {{
                    position: absolute;
                    top: 50%;
                    right: calc(50% - 250px);
                    transform: translateY(-50%);
                    width: 96px;
                    height: 96px;
                    image-rendering: pixelated;
                    animation: fadeIn 2s ease-out;
                    z-index: 10;
                }}
                .main-subtitle {{
                    text-align: center;
                    font-size: 1.4rem;
                    color: #d4af37;
                    font-weight: 300;
                    font-style: italic;
                    margin-top: 0.5rem;
                    margin-bottom: 0.5rem;
                    text-shadow: 0 0 15px rgba(212, 175, 55, 0.5), 0 0 30px rgba(212, 175, 55, 0.2);
                    animation: fadeIn 1.5s ease-out;
                    letter-spacing: 0.5px;
                }}
                .online-status {{
                    text-align: center;
                    font-size: 1.1rem;
                    color: #50c878;
                    margin-bottom: 1.5rem;
                    animation: fadeIn 2s ease-out;
                }}
                .online-status .count {{
                    font-weight: bold;
                    font-size: 1.3rem;
                    text-shadow: 0 0 10px rgba(80, 200, 120, 0.5);
                }}
                @keyframes fadeInDown {{
                    from {{
                        opacity: 0;
                        transform: translateY(-20px);
                    }}
                    to {{
                        opacity: 1;
                        transform: translateY(0);
                    }}
                }}
                @keyframes fadeIn {{
                    from {{
                        opacity: 0;
                    }}
                    to {{
                        opacity: 1;
                    }}
                }}
            </style>
            <div class="main-logo-container">
                <img class="logo" src="data:image/png;base64,{logo_data}" alt="Fibulopedia">
                {"<img class='rotworm-gif' src='data:image/gif;base64," + rotworm_data + "' alt='Rotworm'>" if rotworm_data else ""}
            </div>
            <div class="main-subtitle">
                Your ultimate community hub and knowledge base for Fibula Project
            </div>
        """, unsafe_allow_html=True)
        
        # Note: Online player count feature is disabled due to Cloudflare protection
        # on the MyAAC website preventing automated scraping
    
    # Shortcuts - HIDDEN
    # st.markdown('<p class="shortcuts-title"> Quick Access</p>', unsafe_allow_html=True)
    # col1, col2, col3, col4 = st.columns(4)
    # with col1:
    #     if st.button("📊 Server Info", key="qa_server", use_container_width=True):
    #         st.switch_page("pages/Server_Info.py")
    # with col2:
    #     if st.button("⚔️ Weapons", key="qa_weapons", use_container_width=True):
    #         st.session_state["weapon_filter"] = "All"
    #         st.switch_page("pages/Weapons.py")
    # with col3:
    #     if st.button("🛡️ Equipment", key="qa_equipment", use_container_width=True):
    #         st.session_state["equipment_filter"] = "All"
    #         st.switch_page("pages/Equipment.py")
    # with col4:
    #     if st.button("✨ Spells", key="qa_spells", use_container_width=True):
    #         st.switch_page("pages/Spells.py")
    
    # st.markdown("---")
    
    # Main content area with news on left, search and links on right
    col_main, col_sidebar = st.columns([3, 1])
    
    with col_main:
        # Latest News in the main area
        st.markdown("<h2 style='font-size: 1.5rem;'>► Latest News</h2>", unsafe_allow_html=True)
        
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
                        <h3 style="color: #d4af37; margin: 0.5rem 0; font-size: 1.1rem;">{news['title']}</h3>
                        <p style="color: #ccc; margin: 1rem 0 0 0; font-size: 0.9rem; line-height: 1.5;">{news['content']}</p>
                        <div style="color: #888; font-size: 0.85rem; margin-top: 0.75rem; font-style: italic;">
                            — {news.get('author', 'Admin')}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No news available yet.")
    
    with col_sidebar:
        # Add spacer to align welcome box with Latest News header
        st.markdown("<div style='margin-top: 2.5rem;'></div>", unsafe_allow_html=True)
        
        # Welcome box moved to sidebar
        st.markdown("""
            <style>
            .welcome-box {
                background: linear-gradient(135deg, rgba(30,30,30,0.95), rgba(40,40,40,0.95));
                border: 2px solid #d4af37;
                border-radius: 12px;
                padding: 1.25rem 1.25rem;
                margin: 0 0 1.25rem 0;
                text-align: center;
                box-shadow: 0 4px 20px rgba(212, 175, 55, 0.2);
                animation: fadeInUp 0.8s ease-out;
            }
            .welcome-box h1 {
                color: #d4af37;
                margin-bottom: 0.5rem;
                font-size: 1.6rem;
            }
            .welcome-box p {
                color: #cccccc;
                line-height: 1.5;
                margin-bottom: 0.25rem;
                font-size: 0.9rem;
            }
            </style>
            <div class="welcome-box">
                <h1>Welcome to Fibulopedia</h1>
                <p>Your comprehensive guide to the Fibula Project - a faithful recreation of the classic Tibia 7.1 experience.</p>
                <p>Explore weapons, equipment, spells, monsters, quests, and more.</p>
                <p><i>The website is under construction and may contain incomplete or incorrect information. If you notice any issues, please contact me on Discord.</i></p>
                <p>Molot (Grozze in-game)</p>
            </div>
        """, unsafe_allow_html=True)

        # Quick Search under welcome box
        st.markdown("<h2 style='font-size: 1.3rem;'>⚡ Quick Search</h2>", unsafe_allow_html=True)
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
        st.markdown("<h2 style='font-size: 1.3rem;'>▶ Quick Links</h2>", unsafe_allow_html=True)
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
    create_sidebar_navigation("Home")
    
    main()
    
    create_footer()
