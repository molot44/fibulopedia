"""
Experience Table page for Fibulopedia.

This page displays the required experience points per level.
"""

import streamlit as st

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
setup_page_config("Experience Table", "📊")
load_custom_css()
create_sidebar_navigation()


def main() -> None:
    """Main function to render the experience table page."""
    logger.info("Rendering experience table page")

    # Page header
    create_page_header(
        title="Experience",
        subtitle="This is a list of the experience points that are required to advance to the various levels.",
        icon=""
    )


    # Experience data
    exp_data = [
        (1, 0), (2, 100), (3, 200), (4, 400), (5, 800),
        (6, 1500), (7, 2600), (8, 4200), (9, 6400), (10, 9300),
        (11, 13000), (12, 17600), (13, 23200), (14, 29900), (15, 37800),
        (16, 47000), (17, 57600), (18, 69700), (19, 83400), (20, 98800),
        (21, 116000), (22, 135100), (23, 156200), (24, 179400), (25, 204800),
        (26, 232500), (27, 262600), (28, 295200), (29, 330400), (30, 368300),
        (31, 409000), (32, 452600), (33, 499200), (34, 548900), (35, 601800),
        (36, 658000), (37, 717600), (38, 780700), (39, 847400), (40, 917800),
        (41, 992000), (42, 1070100), (43, 1152200), (44, 1238400), (45, 1328800),
        (46, 1423500), (47, 1522600), (48, 1626200), (49, 1734400), (50, 1847300),
        (51, 1965000), (52, 2087600), (53, 2215200), (54, 2347900), (55, 2485800),
        (56, 2629000), (57, 2777600), (58, 2931700), (59, 3091400), (60, 3256800),
        (61, 3428000), (62, 3605100), (63, 3788200), (64, 3977400), (65, 4172800),
        (66, 4374500), (67, 4582600), (68, 4797200), (69, 5018400), (70, 5246300),
        (71, 5481000), (72, 5722600), (73, 5971200), (74, 6226900), (75, 6489800),
        (76, 6760000), (77, 7037600), (78, 7322700), (79, 7615400), (80, 7915800),
        (81, 8224000), (82, 8540100), (83, 8864200), (84, 9196400), (85, 9536800),
        (86, 9885500), (87, 10242600), (88, 10608200), (89, 10982400), (90, 11365300),
        (91, 11757000), (92, 12157600), (93, 12567200), (94, 12985900), (95, 13413800),
        (96, 13851000), (97, 14297600), (98, 14753700), (99, 15219400), (100, 15694800),
        (101, 16180000), (102, 16675100), (103, 17180200), (104, 17695400), (105, 18220800),
        (106, 18756500), (107, 19302600), (108, 19859200), (109, 20426400), (110, 21004300),
        (111, 21593000), (112, 22192600), (113, 22803200), (114, 23424900), (115, 24057800),
        (116, 24702000), (117, 25357600), (118, 26024700), (119, 26703400), (120, 27393800),
        (121, 28096000), (122, 28810100), (123, 29536200), (124, 30274400), (125, 31024800),
        (126, 31787500), (127, 32562600), (128, 33350200), (129, 34150400), (130, 34963300),
        (131, 35789000), (132, 36627600), (133, 37479200), (134, 38343900), (135, 39221800),
        (136, 40113000), (137, 41017600), (138, 41935700), (139, 42867400), (140, 43812800),
        (141, 44772000), (142, 45745100), (143, 46732200), (144, 47733400), (145, 48748800),
        (146, 49778500), (147, 50822600), (148, 51881200), (149, 52954400), (150, 54042300),
        (151, 55145000), (152, 56262600), (153, 57395200), (154, 58542900), (155, 59705800),
        (156, 60884000), (157, 62077600), (158, 63286700), (159, 64511400), (160, 65751800),
        (161, 67008000), (162, 68280100), (163, 69568200), (164, 70872400), (165, 72192800),
        (166, 73529500), (167, 74882600), (168, 76252200), (169, 77638400), (170, 79041300),
        (171, 80461000), (172, 81897600), (173, 83351200), (174, 84821900), (175, 86309800),
        (176, 87815000), (177, 89337600), (178, 90877700), (179, 92435400), (180, 94010800),
        (181, 95604000), (182, 97215100), (183, 98844200), (184, 100491400), (185, 102156800),
        (186, 103840500), (187, 105542600), (188, 107263200), (189, 109002400), (190, 110760300),
        (191, 112537000), (192, 114332600), (193, 116147200), (194, 117980900), (195, 119833800),
        (196, 121706000), (197, 123597600), (198, 125508700), (199, 127439400), (200, 129389800),
        (201, 131360000), (202, 133350100), (203, 135360200), (204, 137390400), (205, 139440800),
        (206, 141511500), (207, 143602600), (208, 145714200), (209, 147846400), (210, 149999300),
        (211, 152173000), (212, 154367600), (213, 156583200), (214, 158819900), (215, 161077800),
        (216, 163357000), (217, 165657600), (218, 167979700), (219, 170323400), (220, 172688800),
        (221, 175076000), (222, 177485100), (223, 179916200), (224, 182369400), (225, 184844800),
        (226, 187342500), (227, 189862600), (228, 192405200), (229, 194970400), (230, 197558300),
        (231, 200169000), (232, 202802600), (233, 205459200), (234, 208138900), (235, 210841800),
        (236, 213568000), (237, 216317600), (238, 219090700), (239, 221887400), (240, 224707800),
        (241, 227552000), (242, 230420100), (243, 233312200), (244, 236228400), (245, 239168800),
        (246, 242133500), (247, 245122600), (248, 248136200), (249, 251174400), (250, 254237300)
    ]

    # Experience Calculator
    st.markdown("---")
    st.markdown("### 🧮 Experience Calculator")
    st.markdown("Enter your current experience points to see your level and how much exp you need to advance. Optionally, add your exp/h rate to estimate the time needed to reach the next level.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        current_exp = st.number_input(
            "Current Experience",
            min_value=0,
            max_value=254237300,
            value=0,
            step=1000,
            help="Enter your current total experience points"
        )
    
    with col2:
        exp_per_hour = st.number_input(
            "Experience per Hour (optional)",
            min_value=0,
            value=0,
            step=1000,
            help="Enter your average exp/h for time estimation"
        )
    
    # Calculate current level and next level
    if current_exp > 0:
        current_level = 1
        next_level = 2
        exp_to_next = 100
        
        for level, required_exp in exp_data:
            if current_exp >= required_exp:
                current_level = level
                # Find next level
                if level < 250:
                    next_level = level + 1
                    next_level_exp = exp_data[next_level - 1][1]
                    exp_to_next = next_level_exp - current_exp
            else:
                break
        
        # Display results
        st.markdown("---")
        result_html = f"""
        <div style="background-color: #2a2a2a; padding: 20px; border-radius: 8px; border: 2px solid #d4af37; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);">
            <p style="font-size: 18px; color: #e0e0e0; margin: 10px 0;">
                📊 You are currently <strong style="color: #d4af37;">level {current_level}</strong>.
            </p>
            <p style="font-size: 18px; color: #e0e0e0; margin: 10px 0;">
                🎯 You need <strong style="color: #d4af37;">{exp_to_next:,}</strong> more experience to reach level <strong style="color: #d4af37;">{next_level}</strong>.
            </p>
        """
        
        # Add time estimation if exp/h is provided
        if exp_per_hour > 0 and exp_to_next > 0:
            hours_needed = exp_to_next / exp_per_hour
            hours = int(hours_needed)
            minutes = int((hours_needed - hours) * 60)
            
            time_text = ""
            if hours > 0:
                time_text = f"{hours}h {minutes}min"
            else:
                time_text = f"{minutes}min"
            
            result_html += f"""
            <p style="font-size: 18px; color: #e0e0e0; margin: 10px 0;">
                ⏱️ You will reach level <strong style="color: #d4af37;">{next_level}</strong> in approximately <strong style="color: #d4af37;">{time_text}</strong>.
            </p>
            """
        
        result_html += "</div>"
        st.components.v1.html(result_html, height=200)
    
    st.markdown("---")

    # Split data into 5 columns (50 levels each)
    col_size = 50
    columns = [exp_data[i:i + col_size] for i in range(0, len(exp_data), col_size)]

    # Create HTML table
    table_html = """
    <style>
    .exp-table-container {
        width: 100%;
        overflow-x: auto;
        margin: 20px 0;
    }
    .exp-table {
        width: 100%;
        border-collapse: collapse;
        font-family: 'Arial', sans-serif;
        background-color: #1a1a1a;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .exp-table th {
        background: linear-gradient(180deg, #3d3d3d 0%, #2a2a2a 100%);
        color: #d4af37;
        padding: 12px 8px;
        text-align: center;
        font-weight: bold;
        border: 1px solid #4a4a4a;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .exp-table td {
        padding: 10px 12px;
        text-align: center;
        border: 1px solid #333;
        background-color: #2a2a2a;
        color: #e0e0e0;
        font-size: 13px;
    }
    .exp-table tr:hover td {
        background-color: #353535;
    }
    .exp-table tbody tr:nth-child(even) td {
        background-color: #242424;
    }
    .exp-table tbody tr:nth-child(even):hover td {
        background-color: #303030;
    }
    .exp-table td:first-child,
    .exp-table td:nth-child(3),
    .exp-table td:nth-child(5),
    .exp-table td:nth-child(7),
    .exp-table td:nth-child(9) {
        width: 70px;
        font-weight: bold;
        color: #d4af37;
        background-color: #1f1f1f;
    }
    .exp-table tbody tr:nth-child(even) td:first-child,
    .exp-table tbody tr:nth-child(even) td:nth-child(3),
    .exp-table tbody tr:nth-child(even) td:nth-child(5),
    .exp-table tbody tr:nth-child(even) td:nth-child(7),
    .exp-table tbody tr:nth-child(even) td:nth-child(9) {
        background-color: #1a1a1a;
    }
    .exp-table tbody tr:hover td:first-child,
    .exp-table tbody tr:hover td:nth-child(3),
    .exp-table tbody tr:hover td:nth-child(5),
    .exp-table tbody tr:hover td:nth-child(7),
    .exp-table tbody tr:hover td:nth-child(9) {
        background-color: #252525;
    }
    </style>
    <div class="exp-table-container">
        <table class="exp-table">
            <thead>
                <tr>
    """
    
    # Add column headers
    for _ in columns:
        table_html += "<th>Level</th><th>Experience</th>"
    
    table_html += """
                </tr>
            </thead>
            <tbody>
    """
    
    # Add rows
    for row_idx in range(col_size):
        table_html += "<tr>"
        for col in columns:
            if row_idx < len(col):
                level, exp = col[row_idx]
                table_html += f"<td>{level}</td><td>{exp:,}</td>"
            else:
                table_html += "<td></td><td></td>"
        table_html += "</tr>\n"
    
    table_html += """
            </tbody>
        </table>
    </div>
    """
    
    st.components.v1.html(table_html, height=1200, scrolling=True)

    # Footer
    create_footer()


if __name__ == "__main__":
    main()
