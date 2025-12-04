"""
Admin Analytics Dashboard for Fibulopedia - PASSWORD PROTECTED

This page displays website traffic statistics and analytics.
Access is restricted to administrators only.
"""

import streamlit as st
import streamlit_analytics2 as streamlit_analytics
from datetime import datetime

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
setup_page_config("Admin Analytics", "📊")
load_custom_css()


def check_password():
    """Returns True if user entered correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        # SECURE: Password from secrets, NOT hardcoded!
        try:
            ADMIN_PASSWORD = st.secrets["admin_password"]
        except Exception as e:
            st.error("⚠️ Admin password not configured. Check secrets.toml")
            logger.error(f"Error loading admin password: {e}")
            st.session_state["password_correct"] = False
            return
        
        if st.session_state["password"] == ADMIN_PASSWORD:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    # First run, show password input
    if "password_correct" not in st.session_state:
        st.markdown("""
            <div style="text-align: center; padding: 50px 20px;">
                <h1 style="color: #d4af37;">🔒 Admin Access Required</h1>
                <p style="color: #e0e0e0; font-size: 1.1rem;">
                    This page is restricted to administrators only.<br>
                    Please enter the admin password to continue.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input(
                "Admin Password",
                type="password",
                on_change=password_entered,
                key="password",
                placeholder="Enter admin password..."
            )
        return False
    
    # Password incorrect
    elif not st.session_state["password_correct"]:
        st.markdown("""
            <div style="text-align: center; padding: 50px 20px;">
                <h1 style="color: #d4af37;">🔒 Admin Access Required</h1>
                <p style="color: #e0e0e0; font-size: 1.1rem;">
                    This page is restricted to administrators only.<br>
                    Please enter the admin password to continue.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input(
                "Admin Password",
                type="password",
                on_change=password_entered,
                key="password",
                placeholder="Enter admin password..."
            )
            st.error("❌ Incorrect password. Please try again.")
        return False
    
    # Password correct
    else:
        return True


def display_analytics_summary():
    """Display summary statistics in cards."""
    st.markdown("### 📈 Summary Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Get analytics data
    counts = streamlit_analytics.counts
    
    # Calculate metrics - handle different data structures
    total_pageviews = 0
    unique_pages = 0
    
    if counts:
        if isinstance(counts, dict):
            # Check if values are integers or dicts
            for key, value in counts.items():
                if isinstance(value, int):
                    total_pageviews += value
                    unique_pages += 1
                elif isinstance(value, dict):
                    # If nested dict, count the inner values
                    total_pageviews += sum(v for v in value.values() if isinstance(v, int))
                    unique_pages += len(value)
    
    with col1:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%); 
                        padding: 20px; border-radius: 8px; text-align: center;
                        border: 2px solid #5ba3d0; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                <div style="font-size: 2.5rem;">📊</div>
                <div style="font-size: 2rem; font-weight: bold; color: #5ba3d0;">{total_pageviews}</div>
                <div style="color: #e0e0e0; font-size: 0.9rem;">Total Page Views</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%); 
                        padding: 20px; border-radius: 8px; text-align: center;
                        border: 2px solid #a855f7; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                <div style="font-size: 2.5rem;">📄</div>
                <div style="font-size: 2rem; font-weight: bold; color: #a855f7;">{unique_pages}</div>
                <div style="color: #e0e0e0; font-size: 0.9rem;">Unique Pages</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_views = total_pageviews / unique_pages if unique_pages > 0 else 0
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%); 
                        padding: 20px; border-radius: 8px; text-align: center;
                        border: 2px solid #84cc16; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                <div style="font-size: 2.5rem;">📈</div>
                <div style="font-size: 2rem; font-weight: bold; color: #84cc16;">{avg_views:.1f}</div>
                <div style="color: #e0e0e0; font-size: 0.9rem;">Avg Views/Page</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        most_popular = "N/A"
        if counts and isinstance(counts, dict):
            try:
                # Find page with most views, handling nested structures
                max_views = 0
                for key, value in counts.items():
                    if isinstance(value, int) and value > max_views:
                        max_views = value
                        most_popular = key
                    elif isinstance(value, dict):
                        page_total = sum(v for v in value.values() if isinstance(v, int))
                        if page_total > max_views:
                            max_views = page_total
                            most_popular = key
            except:
                most_popular = "N/A"
        
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%); 
                        padding: 20px; border-radius: 8px; text-align: center;
                        border: 2px solid #ff6b35; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                <div style="font-size: 2.5rem;">🔥</div>
                <div style="font-size: 1.2rem; font-weight: bold; color: #ff6b35;">{most_popular}</div>
                <div style="color: #e0e0e0; font-size: 0.9rem;">Most Popular</div>
            </div>
        """, unsafe_allow_html=True)


def display_page_views_table():
    """Display table of page views."""
    st.markdown("### 📑 Page Views Breakdown")
    
    counts = streamlit_analytics.counts
    
    if not counts:
        st.info("No analytics data available yet. Start browsing the site to collect data!")
        return
    
    # Flatten nested structure if needed
    page_views = {}
    if isinstance(counts, dict):
        for key, value in counts.items():
            if isinstance(value, int):
                page_views[key] = value
            elif isinstance(value, dict):
                # Sum nested values
                total = sum(v for v in value.values() if isinstance(v, int))
                page_views[key] = total
    
    if not page_views:
        st.info("No page view data available yet.")
        return
    
    # Sort by views descending
    sorted_pages = sorted(page_views.items(), key=lambda x: x[1], reverse=True)
    
    # Create styled HTML table
    table_html = """
    <style>
    .analytics-table-container {
        width: 100%;
        overflow-x: auto;
        margin: 20px 0;
    }
    .analytics-table {
        width: 100%;
        border-collapse: collapse;
        font-family: 'Arial', sans-serif;
        background-color: #1a1a1a;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .analytics-table thead {
        background-color: #2d2d2d;
    }
    .analytics-table thead th {
        background: linear-gradient(180deg, #3d3d3d 0%, #2a2a2a 100%);
        color: #d4af37;
        padding: 12px 16px;
        text-align: left;
        font-weight: bold;
        border: 1px solid #4a4a4a;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .analytics-table tbody tr {
        border-bottom: 1px solid #333;
    }
    .analytics-table tbody tr:hover {
        background-color: #2a2a2a;
    }
    .analytics-table tbody tr:nth-child(even) {
        background-color: #242424;
    }
    .analytics-table tbody tr:nth-child(even):hover {
        background-color: #303030;
    }
    .analytics-table tbody td {
        padding: 12px 16px;
        text-align: left;
        border: 1px solid #333;
        color: #e0e0e0;
        font-size: 13px;
    }
    .analytics-table tbody td:first-child {
        color: #d4af37;
        font-weight: bold;
    }
    .analytics-table tbody td:last-child {
        text-align: center;
        font-weight: bold;
        color: #5ba3d0;
    }
    .rank-badge {
        display: inline-block;
        background: #d4af37;
        color: #1a1a1a;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: bold;
        margin-right: 8px;
    }
    </style>
    """
    
    table_html += '<div class="analytics-table-container"><table class="analytics-table"><thead><tr>'
    table_html += '<th>Rank</th><th>Page</th><th>Views</th><th>Percentage</th>'
    table_html += '</tr></thead><tbody>'
    
    total_views = sum(page_views.values())
    
    for rank, (page, views) in enumerate(sorted_pages, 1):
        percentage = (views / total_views * 100) if total_views > 0 else 0
        table_html += '<tr>'
        table_html += f'<td><span class="rank-badge">#{rank}</span></td>'
        table_html += f'<td>{page}</td>'
        table_html += f'<td>{views}</td>'
        table_html += f'<td>{percentage:.1f}%</td>'
        table_html += '</tr>'
    
    table_html += '</tbody></table></div>'
    
    st.components.v1.html(table_html, height=min(600, len(sorted_pages) * 50 + 100), scrolling=True)


def display_reset_button():
    """Display button to reset analytics data."""
    st.markdown("---")
    st.markdown("### ⚙️ Analytics Management")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🔄 Reset Analytics", type="secondary", use_container_width=True):
            streamlit_analytics.reset_counts()
            st.success("Analytics data has been reset!")
            st.rerun()
    
    with col2:
        if st.button("📥 Export Data", type="secondary", use_container_width=True):
            st.info("Export functionality coming soon!")


def main() -> None:
    """Main function to render the analytics dashboard page."""
    
    # Check password first
    if not check_password():
        st.stop()
    
    logger.info("Admin accessed analytics dashboard")
    
    # Show sidebar navigation
    create_sidebar_navigation("Admin Analytics")

    # Page header
    create_page_header(
        title="Analytics Dashboard",
        subtitle="Track website traffic and popular content",
        icon="📊"
    )
    
    # Display summary cards
    display_analytics_summary()
    
    st.markdown("---")
    
    # Display page views table
    display_page_views_table()
    
    # Display management buttons
    display_reset_button()
    
    # Info box
    st.markdown("---")
    st.info("""
        **ℹ️ About Analytics**
        
        This dashboard shows page view statistics collected by streamlit-analytics2. 
        Data is stored locally and no personal information is collected. Only page URLs 
        and view counts are tracked to help improve the website experience.
    """)

    # Footer
    create_footer()


if __name__ == "__main__":
    main()
