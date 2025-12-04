"""
Analytics Dashboard for Fibulopedia.

This page displays website analytics including page views, visitor statistics,
and popular content. Data is collected using streamlit-analytics2.
"""

import streamlit as st
import streamlit_analytics2 as streamlit_analytics
from datetime import datetime, timedelta

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
setup_page_config("Analytics Dashboard", "📊")
load_custom_css()
create_sidebar_navigation("Analytics Dashboard")


def display_analytics_summary():
    """Display summary statistics in cards."""
    st.markdown("### 📈 Summary Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Get analytics data
    counts = streamlit_analytics.counts
    
    # Calculate metrics
    total_pageviews = sum(counts.values()) if counts else 0
    unique_pages = len(counts) if counts else 0
    
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
        most_popular = max(counts.items(), key=lambda x: x[1])[0] if counts else "N/A"
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
    
    # Sort by views descending
    sorted_pages = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    
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
    
    total_views = sum(counts.values())
    
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
    logger.info("Rendering analytics dashboard page")

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
