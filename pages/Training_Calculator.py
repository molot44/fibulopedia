"""
Training Calculator page for Fibulopedia.

This page calculates the time needed to train skills based on Tibia 7.1 formulas.
"""

import streamlit as st
import math
import uuid
import streamlit_analytics2 as streamlit_analytics

from src.ui.layout import (
    setup_page_config,
    load_custom_css,
    create_page_header,
    create_sidebar_navigation,
    create_footer
)
from src.logging_utils import setup_logger
from src.analytics_utils import track_page_view

logger = setup_logger(__name__)

# Initialize session ID for analytics
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Start analytics tracking
streamlit_analytics.start_tracking()

# Configure page
setup_page_config("Training Calculator", "")
load_custom_css()
create_sidebar_navigation("Training Calculator")


def calculate_training_time(current_skill: int, current_percent: float, vocation: str, skill_type: str) -> dict:
    """
    Calculate training time needed to reach next skill level.
    
    Formulas:
    - Knight Melee: time_seconds = 50 × 1.1^(skill-10) × (remaining_percent / 100)
    - Knight Shielding: HitsNeeded = 50 × (1000/1100)^(skill-10)
    - Paladin Distance: HitsNeeded = 30 × (1100/1000)^(skill-10)
    - Paladin Shielding: HitsNeeded = 100 × (1000/1100)^(skill-10)
    
    Args:
        current_skill: Current skill level (10-999)
        current_percent: Current progress on skill bar (0-100)
        vocation: Character vocation ("Knight" or "Paladin")
        skill_type: Type of skill ("Melee", "Distance", or "Shielding")
    
    Returns:
        Dictionary with time in various units and assumptions
    """
    
    # Calculate remaining percent to reach next level (100% - current%)
    remaining_percent = 100 - current_percent
    percent_fraction = remaining_percent / 100
    
    if vocation == "Knight" and skill_type == "Melee":
        # Knight Melee formula
        base_constant = 50
        difficulty = math.pow(1.1, current_skill - 10)
        time_seconds = base_constant * difficulty * percent_fraction
        
    elif vocation == "Knight" and skill_type == "Shielding":
        # Knight Shielding formula
        delta = 100
        factor = 1100 / 1000
        
        # Calculate hits needed for full level
        hits_needed_full_level = delta * math.pow(factor, current_skill - 10)
        
        # Apply remaining percent
        hits_needed = hits_needed_full_level * percent_fraction
        
        # Time in minutes (1 hit every 2 seconds)
        time_minutes = (hits_needed * 2) / 60
        time_seconds = time_minutes * 60
        
    elif vocation == "Paladin" and skill_type == "Distance":
        # Paladin Distance formula
        delta = 30
        factor = 1100 / 1000
        
        # Calculate hits needed for full level
        hits_needed_full_level = delta * math.pow(factor, current_skill - 10)
        
        # Apply remaining percent
        hits_needed = hits_needed_full_level * percent_fraction
        
        # Time in minutes (1 hit every 2 seconds)
        time_minutes = (hits_needed * 2) / 60
        time_seconds = time_minutes * 60
        
    elif vocation == "Paladin" and skill_type == "Shielding":
        # Paladin Shielding formula
        delta = 100
        factor = 1100 / 1000
        
        # Calculate hits needed for full level
        hits_needed_full_level = delta * math.pow(factor, current_skill - 10)
        
        # Apply remaining percent
        hits_needed = hits_needed_full_level * percent_fraction
        
        # Time in minutes (1 hit every 2 seconds)
        time_minutes = (hits_needed * 2) / 60
        time_seconds = time_minutes * 60
        
    else:
        # Fallback to Knight Melee if unknown combination
        base_constant = 50
        difficulty = math.pow(1.1, current_skill - 10)
        time_seconds = base_constant * difficulty * percent_fraction
    
    # Convert to various time units
    time_minutes = time_seconds / 60
    time_hours = time_minutes / 60
    time_days = time_hours / 24
    
    return {
        "seconds": round(time_seconds, 2),
        "minutes": round(time_minutes, 2),
        "hours": round(time_hours, 2),
        "days": round(time_days, 2),
        "current_skill": current_skill,
        "next_skill": current_skill + 1,
        "current_percent": current_percent,
        "remaining_percent": remaining_percent,
        "vocation": vocation,
        "skill_type": skill_type
    }


def get_available_skills(vocation: str) -> list:
    """Get available skills for a specific vocation."""
    skill_mapping = {
        "Knight": ["Melee", "Shielding"],
        "Paladin": ["Distance", "Shielding"]
    }
    return skill_mapping.get(vocation, ["Melee"])


def format_time_readable(time_dict: dict) -> str:
    """Convert time dict to human-readable format."""
    days = int(time_dict["days"])
    remaining_hours = time_dict["hours"] - (days * 24)
    hours = int(remaining_hours)
    remaining_minutes = time_dict["minutes"] - (days * 24 * 60) - (hours * 60)
    minutes = int(remaining_minutes)
    seconds = int(time_dict["seconds"] - (days * 24 * 3600) - (hours * 3600) - (minutes * 60))
    
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    
    return ", ".join(parts)


def main() -> None:
    """Main function to render the Training Calculator page."""
    
    # Track page view
    track_page_view("Training Calculator", st.session_state.session_id)
    
    logger.info("Training Calculator page loaded")

    # Page header
    create_page_header(
        title="Training Calculator (work in progress)",
        subtitle="Calculate time needed to train your skills",
        icon=""
    )

    # Introduction
    st.markdown("""
        This calculator helps you estimate how long it will take to train your character's skills.
        Based on authentic Tibia 7.1 training mechanics.
    """)

    st.markdown("---")

    # Calculator section
    st.markdown("### Training Configuration")

    col1, col2 = st.columns(2)

    with col1:
        vocation = st.selectbox(
            "Vocation",
            options=["Knight", "Paladin"],
            help="Select your character's vocation"
        )

    with col2:
        # Get available skills for selected vocation
        available_skills = get_available_skills(vocation)
        skill_type = st.selectbox(
            "Skill Type",
            options=available_skills,
            help="Select the skill you want to train"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        current_skill_input = st.text_input(
            "Current Skill Level",
            value="50",
            help="Enter your current skill level (10-999)",
            placeholder="Enter skill level (10-999)"
        )
        
        # Validate input
        try:
            current_skill = int(current_skill_input)
            if current_skill < 10:
                st.error("⚠️ Skill level must be at least 10.")
                current_skill = 10
            elif current_skill > 999:
                st.error("⚠️ Skill level cannot exceed 999.")
                current_skill = 999
        except ValueError:
            st.error("⚠️ Please enter a valid number.")
            current_skill = 50

    with col4:
        current_percent = st.slider(
            "Current Skill Progress (%)",
            min_value=0,
            max_value=100,
            value=0,
            step=1,
            help="Your current progress on the skill bar (0 = start of bar, 100 = end of bar)"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Calculate button
    if st.button("Calculate Training Time", type="primary", use_container_width=True):
        # Calculate training time
        result = calculate_training_time(current_skill, current_percent, vocation, skill_type)
            
        # Display results
        st.markdown("---")
        st.markdown("### Training Results")
        
        # Main result card
        st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
                border: 2px solid #d4af37;
                border-radius: 10px;
                padding: 25px;
                margin: 20px 0;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            '>
                <div style='text-align: center;'>
                    <div style='font-size: 1.2rem; color: #d4af37; margin-bottom: 10px;'>
                        ⏱️ <strong>Estimated Training Time</strong>
                    </div>
                    <div style='font-size: 2.5rem; font-weight: bold; color: #e0e0e0; margin: 15px 0;'>
                        {format_time_readable(result)}
                    </div>
                    <div style='color: #a0a0a0; font-size: 0.95rem; margin-top: 10px;'>
                        To reach skill {result['next_skill']} from {result['current_skill']} ({result['current_percent']}%)
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
            
        # Detailed breakdown
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.markdown(f"""
                <div style='
                    background: #2a2a2a;
                    border: 1px solid #444;
                    border-radius: 8px;
                    padding: 15px;
                    text-align: center;
                '>
                    <div style='color: #888; font-size: 0.9rem;'>Total Hours</div>
                    <div style='color: #5ba3d0; font-size: 1.8rem; font-weight: bold;'>
                        {result['hours']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_b:
            st.markdown(f"""
                <div style='
                    background: #2a2a2a;
                    border: 1px solid #444;
                    border-radius: 8px;
                    padding: 15px;
                    text-align: center;
                '>
                    <div style='color: #888; font-size: 0.9rem;'>Total Minutes</div>
                    <div style='color: #84cc16; font-size: 1.8rem; font-weight: bold;'>
                        {result['minutes']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_c:
            st.markdown(f"""
                <div style='
                    background: #2a2a2a;
                    border: 1px solid #444;
                    border-radius: 8px;
                    padding: 15px;
                    text-align: center;
                '>
                    <div style='color: #888; font-size: 0.9rem;'>Total Seconds</div>
                    <div style='color: #a855f7; font-size: 1.8rem; font-weight: bold;'>
                        {result['seconds']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    create_footer()


if __name__ == "__main__":
    try:
        main()
    finally:
        streamlit_analytics.stop_tracking()
