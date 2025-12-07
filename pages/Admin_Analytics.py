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
from src.analytics_utils import (
    get_page_views,
    get_total_page_views,
    get_unique_sessions,
    get_analytics_summary,
    reset_analytics
)

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
    
    # Get our custom analytics data
    summary = get_analytics_summary()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
                border: 2px solid #d4af37;
                border-radius: 8px;
                padding: 1.5rem;
                text-align: center;
            '>
                <div style='font-size: 2.5rem; font-weight: bold; color: #d4af37;'>
                    {summary['total_page_views']}
                </div>
                <div style='font-size: 0.9rem; color: #888; margin-top: 0.5rem;'>
                    Total Page Views
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
                border: 2px solid #5ba3d0;
                border-radius: 8px;
                padding: 1.5rem;
                text-align: center;
            '>
                <div style='font-size: 2.5rem; font-weight: bold; color: #5ba3d0;'>
                    {summary['unique_sessions']}
                </div>
                <div style='font-size: 0.9rem; color: #888; margin-top: 0.5rem;'>
                    Unique Visitors
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
                border: 2px solid #50c878;
                border-radius: 8px;
                padding: 1.5rem;
                text-align: center;
            '>
                <div style='font-size: 2.5rem; font-weight: bold; color: #50c878;'>
                    {summary['pages_tracked']}
                </div>
                <div style='font-size: 0.9rem; color: #888; margin-top: 0.5rem;'>
                    Pages Tracked
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
                border: 2px solid #e67e22;
                border-radius: 8px;
                padding: 1.5rem;
                text-align: center;
            '>
                <div style='font-size: 2.5rem; font-weight: bold; color: #e67e22;'>
                    {summary['avg_pages_per_session']}
                </div>
                <div style='font-size: 0.9rem; color: #888; margin-top: 0.5rem;'>
                    Avg Pages/Visit
                </div>
            </div>
        """, unsafe_allow_html=True)


def display_page_views_table():
    """Display table of page views."""
    st.markdown("### 📑 Page Views Breakdown")
    
    # Get our custom analytics data
    page_views = get_page_views()
    
    if not page_views:
        st.info("No page view data available yet. Start browsing the site to collect data!")
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
        if st.button("🔄 Reset Page Analytics", type="secondary", use_container_width=True):
            reset_analytics()
            st.success("Page analytics data has been reset!")
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset Widget Analytics", type="secondary", use_container_width=True):
            streamlit_analytics.reset_counts()
            st.success("Widget analytics data has been reset!")
            st.rerun()


def display_page_popularity_chart():
    """Display bar chart of page popularity."""
    st.markdown("### 📊 Page Popularity")
    
    # Get our custom analytics data
    page_views = get_page_views()
    
    if not page_views:
        st.info("No page view data available yet.")
        return
    
    # Sort by views
    sorted_pages = sorted(page_views.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Create bar chart data
    import pandas as pd
    df = pd.DataFrame(sorted_pages, columns=["Page", "Views"])
    
    st.bar_chart(df.set_index("Page"))


def display_session_statistics():
    """Display session-related statistics."""
    st.markdown("### ⏱️ Session Statistics")
    
    # Get our custom analytics data
    summary = get_analytics_summary()
    total_page_views = summary['total_page_views']
    unique_sessions = summary['unique_sessions']
    avg_pages = summary['avg_pages_per_session']
    
    col1, col2, col3 = st.columns(3)
        
    with col1:
        st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, rgba(30,30,30,0.95), rgba(40,40,40,0.95));
                border: 2px solid #d4af37;
                border-radius: 8px;
                padding: 1.5rem;
                text-align: center;
            '>
                <div style='color: #d4af37; font-size: 2.5rem; font-weight: bold;'>
                    {unique_sessions}
                </div>
                <div style='color: #888; font-size: 0.9rem; margin-top: 0.5rem;'>
                    Unique Sessions
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, rgba(30,30,30,0.95), rgba(40,40,40,0.95));
                border: 2px solid #5ba3d0;
                border-radius: 8px;
                padding: 1.5rem;
                text-align: center;
            '>
                <div style='color: #5ba3d0; font-size: 2.5rem; font-weight: bold;'>
                    {total_page_views}
                </div>
                <div style='color: #888; font-size: 0.9rem; margin-top: 0.5rem;'>
                    Total Page Views
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, rgba(30,30,30,0.95), rgba(40,40,40,0.95));
                border: 2px solid #50c878;
                border-radius: 8px;
                padding: 1.5rem;
                text-align: center;
            '>
                <div style='color: #50c878; font-size: 2.5rem; font-weight: bold;'>
                    {avg_pages}
                </div>
                <div style='color: #888; font-size: 0.9rem; margin-top: 0.5rem;'>
                    Avg Pages/Session
                </div>
            </div>
        """, unsafe_allow_html=True)


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
    
    # Add refresh button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Refresh Statistics", use_container_width=True, type="primary"):
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display summary cards
    display_analytics_summary()
    
    st.markdown("---")
    
    # Display session statistics
    display_session_statistics()
    
    st.markdown("---")
    
    # Display page popularity chart
    display_page_popularity_chart()
    
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
        Data is stored locally and no personal information is collected. Only session IDs 
        (randomly generated UUIDs) and page view counts are tracked to help improve the 
        website experience. No personal information, IP addresses, or cookies are collected.
    """)

    # Footer
    create_footer()


if __name__ == "__main__":
    main()
