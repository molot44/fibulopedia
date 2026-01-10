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
import uuid
import streamlit_analytics2 as streamlit_analytics

from src.config import APP_TITLE, APP_SUBTITLE, APP_ICON
from src.ui.layout import (
    setup_page_config,
    load_custom_css,
    create_sidebar_navigation,
    create_footer
)
from src.logging_utils import setup_logger
from src.services.fibula_status import fetch_online_count
from src.analytics_utils import track_page_view
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
    
    # Track page view
    session_id = st.session_state.get("session_id")
    track_page_view("Home", session_id)
    
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
                    "event": "#ff6347",
                    "interview": "#9b59b6"
                }
                badge_color = category_colors.get(news.get("category", "info"), "#ffd700")
                
                # Check if news has modal
                has_modal = news.get("hasModal", False)
                
                # Check if this is the interview news (id=5) to add image
                if news.get('id') == 5:
                    # Load interview banner image
                    interview_banner_path = Path("assets/interview_erik/interview_banner_small.png")
                    interview_banner_data = ""
                    if interview_banner_path.exists():
                        with open(interview_banner_path, "rb") as f:
                            interview_banner_data = base64.b64encode(f.read()).decode()
                    
                    st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, rgba(30,30,30,0.95), rgba(40,40,40,0.95));
                            border-left: 3px solid #d4af37;
                            border-radius: 8px;
                            padding: 1.5rem;
                            margin-bottom: 1rem;
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
                            <div style="display: flex; gap: 1.5rem; align-items: flex-start;">
                                <div style="flex: 1; min-width: 0;">
                                    <h3 style="color: #d4af37; margin: 0.5rem 0; font-size: 1.1rem;">{news['title']}</h3>
                                    <p style="color: #ccc; margin: 1rem 0 0 0; font-size: 0.9rem; line-height: 1.5;">{news['content']}</p>
                                    <div style="color: #888; font-size: 0.85rem; margin-top: 0.75rem; font-style: italic;">
                                        — {news.get('author', 'Admin')}
                                    </div>
                                </div>
                                <div style="flex-shrink: 0; margin-top: 1rem;">
                                    <img src="data:image/png;base64,{interview_banner_data}" 
                                         alt="Interview Banner" 
                                         style="width: 280px; border-radius: 6px; object-fit: cover;">
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, rgba(30,30,30,0.95), rgba(40,40,40,0.95));
                            border-left: 3px solid #d4af37;
                            border-radius: 8px;
                            padding: 1.5rem;
                            margin-bottom: 1rem;
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
                
                # If news has modal, create a button to open it
                if has_modal:
                    if st.button(f"Read Full Interview", key=f"btn_{news['id']}", use_container_width=True):
                        st.session_state[f"show_modal_{news['id']}"] = True
                    
                    # Show modal if triggered
                    if st.session_state.get(f"show_modal_{news['id']}", False):
                        modal_data = news.get("modalContent", {})
                        
                        # Load interview banner for modal
                        modal_banner_path = Path("assets/interview_erik/interview_banner.png")
                        modal_banner_data = ""
                        if modal_banner_path.exists():
                            with open(modal_banner_path, "rb") as f:
                                modal_banner_data = base64.b64encode(f.read()).decode()
                        
                        # Replace the banner image path in content with base64
                        modal_content = modal_data.get('content', '')
                        modal_content = modal_content.replace(
                            "assets/interview_erik/interview_banner.png",
                            f"data:image/png;base64,{modal_banner_data}"
                        )
                        
                        @st.dialog(modal_data.get("title", news["title"]), width="large")
                        def show_interview():
                            st.markdown(f"""
                                <style>
                                    .interview-content h3 {{
                                        color: #d4af37;
                                        font-size: 1.5rem;
                                        font-weight: bold;
                                        margin-top: 3rem;
                                        margin-bottom: 1.5rem;
                                        padding-bottom: 0.5rem;
                                        border-bottom: 2px solid #d4af37;
                                    }}
                                    .interview-content h4 {{
                                        color: #d4af37;
                                        font-size: 1.1rem;
                                        font-weight: bold;
                                        margin-top: 1.5rem;
                                        margin-bottom: 0.75rem;
                                    }}
                                    .interview-content p {{
                                        margin-bottom: 1.25rem;
                                    }}
                                    .interview-content blockquote.pull-quote {{
                                        margin: 2.5rem 0;
                                    }}
                                </style>
                                <div style="
                                    color: #d4af37;
                                    font-size: 1.2rem;
                                    font-style: italic;
                                    margin-bottom: 2rem;
                                    border-left: 3px solid #d4af37;
                                    padding-left: 1rem;
                                ">
                                    {modal_data.get('subtitle', '')}
                                </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown(f"""
                                <div class="interview-content" style="
                                    color: #ccc;
                                    font-size: 1rem;
                                    line-height: 1.8;
                                ">
                                    {modal_content}
                                </div>
                            """, unsafe_allow_html=True)
                        
                        show_interview()
                        # Clear the flag after modal closes
                        st.session_state[f"show_modal_{news['id']}"] = False
                    
                    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
        else:
            st.info("No news available yet.")
    
    with col_sidebar:
        # Add spacer to align welcome box with Latest News header
        st.markdown("<div style='margin-top: 2.5rem;'></div>", unsafe_allow_html=True)
        
        # Welcome box moved to sidebar with avatar
        grozze_path = Path("assets/grozze.png")
        grozze_data = ""
        if grozze_path.exists():
            with open(grozze_path, "rb") as f:
                grozze_data = base64.b64encode(f.read()).decode()
        
        st.markdown(f"""
            <style>
            .welcome-box {{
                background: linear-gradient(135deg, rgba(30,30,30,0.95), rgba(40,40,40,0.95));
                border: 2px solid #d4af37;
                border-radius: 12px;
                padding: 1.25rem 1.25rem;
                margin: 0 0 1.25rem 0;
                text-align: center;
                box-shadow: 0 4px 20px rgba(212, 175, 55, 0.2);
                animation: fadeInUp 0.8s ease-out;
            }}
            .welcome-box h1 {{
                color: #d4af37;
                margin-bottom: 0.5rem;
                font-size: 1.6rem;
            }}
            .welcome-box p {{
                color: #cccccc;
                line-height: 1.5;
                margin-bottom: 0.25rem;
                font-size: 0.9rem;
            }}
            .welcome-box img.avatar {{
                width: 160px;
                height: 160px;
                border-radius: 50%;
                border: 3px solid #d4af37;
                margin-bottom: 0.75rem;
                box-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
                transition: transform 0.3s ease;
            }}
            .welcome-box img.avatar:hover {{
                transform: scale(1.1);
            }}
            </style>
            <div class="welcome-box">
                {"<img class='avatar' src='data:image/png;base64," + grozze_data + "' alt='Grozze'>" if grozze_data else ""}
                <h1>Welcome to Fibulopedia</h1>
                <p>Your comprehensive guide to the Fibula Project - a faithful recreation of the classic Tibia 7.1 experience.</p>
                <p>Explore weapons, equipment, spells, monsters, quests, and more.</p>
                <p>Molot (Grozze in-game)</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Quick Links section
        st.markdown("<h2 style='font-size: 1.3rem;'>▶ Quick Links</h2>", unsafe_allow_html=True)
        st.markdown("""
            <div style="
                background: rgba(40,40,40,0.4);
                border: 2px solid #d4af37;
                border-radius: 8px;
                padding: 1.5rem;
                text-align: center;
            ">
                <p style="margin: 0.5rem 0;">
                    <a href="https://amera.fibula.app/" target="_blank" style="color: #d4af37; text-decoration: none; font-size: 1.1rem; font-weight: bold;">
                        🌐 Project Fibula Official Website
                    </a>
                </p>
                <p style="margin: 0.5rem 0;">
                    <a href="https://discord.gg/Jzz6yUme" target="_blank" style="color: #7289da; text-decoration: none; font-size: 1.1rem; font-weight: bold;">
                        💬 Project Fibula Discord
                    </a>
                </p>
            </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    setup_page_config("Home", APP_ICON, layout="wide")
    load_custom_css()
    
    # Initialize analytics with session tracking
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    # Start analytics tracking before any interactive elements
    streamlit_analytics.start_tracking()
    
    create_sidebar_navigation("Home")
    
    try:
        main()
    finally:
        # Stop analytics tracking
        streamlit_analytics.stop_tracking()
    
    create_footer()
