"""
Magic Damage Calculator page for Fibulopedia.

This page calculates damage output for all magic spells and runes based on character level and magic level.
"""

import streamlit as st
import pandas as pd
import math

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
setup_page_config("Magic Damage Calculator", "")
load_custom_css()
create_sidebar_navigation("Magic Damage Calculator")


def calculate_spell_damage(level: int, mlvl: int, spell_type: str) -> dict:
    """Calculate min and max damage for a spell based on Tibia 7.1 formulas from TibiaWiki."""
    
    # Base calculation with floor function
    base = math.floor(level * 0.2)
    
    # Attack Runes - using base formula: ⌊lvl×0.2⌋ + (mlvl × x) + y
    attack_runes = {
        "Light Magic Missile": {
            "formula": (0.81, 4, 0.4, 2),
            "mana": 40,
            "type": "Single Target",
            "element": "Energy"
        },
        "Heavy Magic Missile": {
            "formula": (1.59, 10, 0.81, 4),
            "mana": 70,
            "type": "Single Target",
            "element": "Energy"
        },
        "Fireball": {
            "formula": (3.0, 18, 1.81, 10),
            "mana": 60,
            "type": "Area (3x3)",
            "element": "Fire"
        },
        "Great Fireball": {
            "formula": (2.8, 17, 1.2, 7),
            "mana": 120,
            "type": "Area (3x3)",
            "element": "Fire"
        },
        "Sudden Death": {
            "formula": (7.395, 46, 4.605, 28),
            "mana": 220,
            "type": "Single Target",
            "element": "Physical"
        }
    }
    
    # Explosion uses old formula: lvl/5 + mlvl × c
    old_formula_spells = {
        "Explosion": {
            "formula": (4.8, 0.0),  # (max_mult, min_mult)
            "mana": 180,
            "type": "Area (3x3)",
            "element": "Physical"
        }
    }
    
    # Instant Spells - using base formula: ⌊lvl×0.2⌋ + (mlvl × x) + y
    instant_spells = {
        "Exori Vis": {  # Strike Spells
            "formula": (2.203, 13, 1.403, 8),
            "mana": 20,
            "type": "Single Target",
            "element": "Energy"
        },
        "Exevo Vis Lux": {  # Energy Beam
            "formula": (4.0, 0, 2.5, 0),  # Using old formula pattern converted
            "mana": 100,
            "type": "Beam",
            "element": "Energy",
            "old_formula": True
        },
        "Exevo Gran Vis Lux": {  # Great Energy Beam
            "formula": (7.0, 0, 4.0, 0),  # Using old formula pattern converted
            "mana": 200,
            "type": "Beam",
            "element": "Energy",
            "old_formula": True
        },
        "Exevo Gran Mas Vis": {  # Rage of the Skies
            "formula": (12.0, 0, 5.0, 0),  # Using old formula pattern converted
            "mana": 800,
            "type": "Area (Large)",
            "element": "Energy",
            "old_formula": True
        }
    }
    
    # Spells with unknown formulas
    unknown_formula_spells = {
        "Exevo Mort Hur": {
            "mana": 250,
            "type": "Unknown",
            "element": "Death"
        }
    }
    
    # Calculate damage for attack runes
    if spell_type in attack_runes:
        data = attack_runes[spell_type]
        x_max, y_max, x_min, y_min = data["formula"]
        max_dmg = base + int(mlvl * x_max) + y_max
        min_dmg = base + int(mlvl * x_min) + y_min
        
        return {
            "min": int(min_dmg),
            "max": int(max_dmg),
            "avg": (min_dmg + max_dmg) / 2,
            "mana": data["mana"],
            "dmg_per_mana": ((min_dmg + max_dmg) / 2) / data["mana"] if data["mana"] > 0 else 0,
            "type": data["type"],
            "element": data["element"]
        }
    
    # Calculate damage for old formula spells
    elif spell_type in old_formula_spells:
        data = old_formula_spells[spell_type]
        d_max, c_min = data["formula"]
        base_old = int(level / 5)
        max_dmg = base_old + int(mlvl * d_max)
        min_dmg = base_old + int(mlvl * c_min)
        
        return {
            "min": int(min_dmg),
            "max": int(max_dmg),
            "avg": (min_dmg + max_dmg) / 2,
            "mana": data["mana"],
            "dmg_per_mana": ((min_dmg + max_dmg) / 2) / data["mana"] if data["mana"] > 0 else 0,
            "type": data["type"],
            "element": data["element"]
        }
    
    # Calculate damage for instant spells
    elif spell_type in instant_spells:
        data = instant_spells[spell_type]
        
        # Check if using old formula
        if data.get("old_formula"):
            d_max, _, c_min, _ = data["formula"]
            base_old = int(level / 5)
            max_dmg = base_old + int(mlvl * d_max)
            min_dmg = base_old + int(mlvl * c_min)
        else:
            x_max, y_max, x_min, y_min = data["formula"]
            max_dmg = base + int(mlvl * x_max) + y_max
            min_dmg = base + int(mlvl * x_min) + y_min
        
        return {
            "min": int(min_dmg),
            "max": int(max_dmg),
            "avg": (min_dmg + max_dmg) / 2,
            "mana": data["mana"],
            "dmg_per_mana": ((min_dmg + max_dmg) / 2) / data["mana"] if data["mana"] > 0 else 0,
            "type": data["type"],
            "element": data["element"]
        }
    
    # Handle spells with unknown formulas
    elif spell_type in unknown_formula_spells:
        data = unknown_formula_spells[spell_type]
        return {
            "min": "??",
            "max": "??",
            "avg": "??",
            "mana": data["mana"],
            "dmg_per_mana": "??",
            "type": data["type"],
            "element": data["element"]
        }
    
    return None


def main() -> None:
    """Main function to render the magic damage calculator page."""
    logger.info("Rendering magic damage calculator page")

    # Page header
    create_page_header(
        title="Magic Damage Calculator",
        subtitle="Calculate spell and rune damage based on your level and magic level",
        icon=""
    )

    # Input section
    st.markdown("### Character Stats")
    col1, col2 = st.columns(2)
    
    with col1:
        character_level = st.number_input(
            "Character Level",
            min_value=1,
            max_value=300,
            value=50,
            step=1,
            help="Your character's level"
        )
    
    with col2:
        magic_level = st.number_input(
            "Magic Level",
            min_value=0,
            max_value=150,
            value=50,
            step=1,
            help="Your magic level"
        )

    # Calculate all spells
    if character_level > 0:
        st.markdown("---")
        st.markdown("### Damage Results")
        st.markdown("All damage values are calculated based on your character stats.")
        
        # Prepare data for all spells
        spell_categories = {
            "Attack Runes": [
                "Light Magic Missile", "Heavy Magic Missile", "Fireball",
                "Great Fireball", "Explosion", "Sudden Death"
            ],
            "Spells": [
                "Exori Vis", "Exevo Vis Lux", "Exevo Gran Vis Lux",
                "Exevo Mort Hur", "Exevo Gran Mas Vis"
            ]
        }
        
        for category, spells in spell_categories.items():
            st.markdown(f"#### {category}")
            
            results_data = []
            for spell_name in spells:
                result = calculate_spell_damage(character_level, magic_level, spell_name)
                if result:
                    # Handle unknown formulas that return string values
                    avg_damage = result['avg'] if isinstance(result['avg'], str) else f"{result['avg']:.1f}"
                    dmg_per_mana = result['dmg_per_mana'] if isinstance(result['dmg_per_mana'], str) else f"{result['dmg_per_mana']:.2f}"
                    
                    results_data.append({
                        "Spell/Rune": spell_name,
                        "Type": result["type"],
                        "Element": result["element"],
                        "Min Damage": result["min"],
                        "Max Damage": result["max"],
                        "Avg Damage": avg_damage,
                        "Mana Cost": result["mana"]
                    })
            
            if results_data:
                df = pd.DataFrame(results_data)
                
                # Create styled HTML table
                table_html = """
                <style>
                .calc-table-container {
                    width: 100%;
                    overflow-x: auto;
                    margin: 5px 0;
                }
                .calc-table {
                    width: 100%;
                    border-collapse: collapse;
                    font-family: 'Arial', sans-serif;
                    background-color: #1a1a1a;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                }
                .calc-table thead {
                    background-color: #2d2d2d;
                }
                .calc-table thead th {
                    background: linear-gradient(180deg, #3d3d3d 0%, #2a2a2a 100%);
                    color: #d4af37;
                    padding: 12px 8px;
                    text-align: center;
                    font-weight: bold;
                    border: 1px solid #4a4a4a;
                    font-size: 13px;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }
                .calc-table tbody tr {
                    border-bottom: 1px solid #333;
                }
                .calc-table tbody tr:hover {
                    background-color: #2a2a2a;
                }
                .calc-table tbody tr:nth-child(even) {
                    background-color: #242424;
                }
                .calc-table tbody tr:nth-child(even):hover {
                    background-color: #303030;
                }
                .calc-table tbody td {
                    padding: 10px 8px;
                    text-align: center;
                    border: 1px solid #333;
                    color: #e0e0e0;
                    font-size: 13px;
                }
                .calc-table tbody td:first-child {
                    text-align: left;
                    font-weight: bold;
                    color: #d4af37;
                }
                .element-fire { color: #ff6b35; }
                .element-ice { color: #5ba3d0; }
                .element-energy { color: #a855f7; }
                .element-earth { color: #84cc16; }
                .element-death { color: #dc2626; }
                .element-physical { color: #9ca3af; }
                </style>
                """
                
                table_html += '<div class="calc-table-container"><table class="calc-table"><thead><tr>'
                for col in df.columns:
                    table_html += f'<th>{col}</th>'
                table_html += '</tr></thead><tbody>'
                
                for _, row in df.iterrows():
                    table_html += '<tr>'
                    for idx, (col, val) in enumerate(row.items()):
                        if col == "Element":
                            element_class = f"element-{val.lower()}"
                            table_html += f'<td class="{element_class}">{val}</td>'
                        else:
                            table_html += f'<td>{val}</td>'
                    table_html += '</tr>'
                
                table_html += '</tbody></table></div>'
                
                st.components.v1.html(table_html, height=400, scrolling=True)

    # Footer
    create_footer()


if __name__ == "__main__":
    main()
