"""
Map page for Fibulopedia.

This page displays the Tibia 7.1 world maps.
"""

import streamlit as st
from pathlib import Path
import base64

from src.config import MAP_PATH, ASSETS_DIR
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
setup_page_config("Maps", "🗺️")
load_custom_css()
create_sidebar_navigation("Map")


def get_image_base64(image_path: Path) -> str:
    """Convert image to base64 for embedding."""
    try:
        with open(image_path, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    except Exception as e:
        logger.error(f"Error loading image {image_path}: {e}")
        return ""


def main() -> None:
    """Main function to render the maps page."""
    logger.info("Rendering maps page")

    # Page header
    create_page_header(
        title="Tibia Maps",
        subtitle="Classic Tibia 7.1 maps",
        icon=""
    )

    # Define map paths
    map1_path = MAP_PATH  # Original map
    map2_path = ASSETS_DIR / "Map_7.1_new.jpg"  # New map
    rook_path = ASSETS_DIR / "rookgaard_map.png"  # Rookgaard map

    # Check if maps exist
    if map1_path.exists() and map2_path.exists() and rook_path.exists():
        # Convert images to base64
        map1_base64 = get_image_base64(map1_path)
        map2_base64 = get_image_base64(map2_path)
        rook_base64 = get_image_base64(rook_path)
        
        # Create interactive map gallery with working modal
        maps_html = f"""
        <style>
        .map-gallery {{
            display: flex;
            gap: 20px;
            margin: 20px 0;
            justify-content: center;
            flex-wrap: wrap;
            align-items: flex-start;
        }}
        .map-item {{
            flex: 0 1 auto;
            max-width: 500px;
            cursor: pointer;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .map-item:hover {{
            transform: scale(1.05);
            box-shadow: 0 8px 16px rgba(212, 175, 55, 0.5);
        }}
        .map-item img {{
            width: 100%;
            height: auto;
            display: block;
        }}
        .map-title {{
            text-align: center;
            color: #d4af37;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        /* Modal styles */
        .map-modal {{
            display: none;
            position: fixed;
            z-index: 999999;
            left: 0;
            top: 0;
            width: 100vw;
            height: 100vh;
            max-height: 100vh;
            background-color: rgba(0, 0, 0, 0.95);
            overflow: hidden;
        }}
        .map-modal.show {{
            display: block;
        }}
        .map-modal-container {{
            width: 100%;
            height: 100%;
            position: relative;
            overflow: hidden;
            padding: 60px 20px 20px 20px;
        }}
        .map-modal-content {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(1);
            cursor: move;
            transition: transform 0.05s ease-out;
            transform-origin: center center;
        }}
        .map-modal-close {{
            position: fixed;
            top: 20px;
            right: 35px;
            color: #d4af37;
            font-size: 50px;
            font-weight: bold;
            cursor: pointer;
            z-index: 1000000;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
            transition: color 0.3s ease;
            background: rgba(0, 0, 0, 0.7);
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            line-height: 1;
        }}
        .map-modal-close:hover {{
            color: #fff;
            background: rgba(0, 0, 0, 0.9);
        }}
        .zoom-info {{
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            color: #d4af37;
            background: rgba(0, 0, 0, 0.7);
            padding: 10px 20px;
            border-radius: 4px;
            font-size: 14px;
            z-index: 1000000;
        }}
        </style>
        
        <div class="map-gallery">
            <div class="map-item" onclick="openMapModal('modal1')">
                <div class="map-title">Tibia 7.1 world map</div>
                <img src="data:image/png;base64,{map1_base64}" alt="Classic Map">
            </div>
            <div class="map-item" onclick="openMapModal('modal2')">
                <div class="map-title">Tibia 7.1 world map with labels</div>
                <img src="data:image/jpeg;base64,{map2_base64}" alt="New Map">
            </div>
            <div class="map-item" onclick="openMapModal('modal3')">
                <div class="map-title">Rookgaard map</div>
                <img src="data:image/png;base64,{rook_base64}" alt="Rookgaard Map">
            </div>
        </div>
        
        <div id="modal1" class="map-modal">
            <span class="map-modal-close" onclick="closeMapModal('modal1')">&times;</span>
            <div class="zoom-info">Use scroll wheel to zoom • Drag to pan</div>
            <div class="map-modal-container" id="container1">
                <img class="map-modal-content" id="modalImg1" src="data:image/png;base64,{map1_base64}" alt="Classic Map Full Size">
            </div>
        </div>
        
        <div id="modal2" class="map-modal">
            <span class="map-modal-close" onclick="closeMapModal('modal2')">&times;</span>
            <div class="zoom-info">Use scroll wheel to zoom • Drag to pan</div>
            <div class="map-modal-container" id="container2">
                <img class="map-modal-content" id="modalImg2" src="data:image/jpeg;base64,{map2_base64}" alt="New Map Full Size">
            </div>
        </div>
        
        <div id="modal3" class="map-modal">
            <span class="map-modal-close" onclick="closeMapModal('modal3')">&times;</span>
            <div class="zoom-info">Use scroll wheel to zoom • Drag to pan</div>
            <div class="map-modal-container" id="container3">
                <img class="map-modal-content" id="modalImg3" src="data:image/png;base64,{rook_base64}" alt="Rookgaard Map Full Size">
            </div>
        </div>
        
        <script>
        let scale1 = 1, scale2 = 1, scale3 = 1;
        let offsetX1 = 0, offsetY1 = 0;
        let offsetX2 = 0, offsetY2 = 0;
        let offsetX3 = 0, offsetY3 = 0;
        let isPanning = false;
        let startX = 0, startY = 0;
        let currentModalId = null;
        
        function openMapModal(modalId) {{
            var modal = document.getElementById(modalId);
            if (modal) {{
                modal.classList.add('show');
                document.body.style.overflow = 'hidden';
                
                // Reset scale and position
                if (modalId === 'modal1') {{
                    scale1 = 1;
                    offsetX1 = 0;
                    offsetY1 = 0;
                }} else if (modalId === 'modal2') {{
                    scale2 = 1;
                    offsetX2 = 0;
                    offsetY2 = 0;
                }} else if (modalId === 'modal3') {{
                    scale3 = 1;
                    offsetX3 = 0;
                    offsetY3 = 0;
                }}
                
                var img = modal.querySelector('.map-modal-content');
                img.style.transform = 'translate(-50%, -50%) scale(1)';
                currentModalId = modalId;
            }}
        }}
        
        function closeMapModal(modalId) {{
            var modal = document.getElementById(modalId);
            if (modal) {{
                modal.classList.remove('show');
                document.body.style.overflow = 'auto';
                currentModalId = null;
            }}
        }}
        
        // Zoom and pan with cursor-centered zoom
        function setupZoom(modalId, imgId) {{
            var modal = document.getElementById(modalId);
            var img = document.getElementById(imgId);
            var container = modal.querySelector('.map-modal-container');
            
            container.addEventListener('wheel', function(e) {{
                e.preventDefault();
                
                let scale = modalId === 'modal1' ? scale1 : (modalId === 'modal2' ? scale2 : scale3);
                let offsetX = modalId === 'modal1' ? offsetX1 : (modalId === 'modal2' ? offsetX2 : offsetX3);
                let offsetY = modalId === 'modal1' ? offsetY1 : (modalId === 'modal2' ? offsetY2 : offsetY3);

                var rect = container.getBoundingClientRect();
                var cx = rect.width / 2;
                var cy = rect.height / 2;

                // mouse position relative to container center
                var mouseX = e.clientX - rect.left;
                var mouseY = e.clientY - rect.top;
                var dx = mouseX - cx;
                var dy = mouseY - cy;

                // image coords under cursor before zoom
                var imgX = (dx - offsetX) / scale;
                var imgY = (dy - offsetY) / scale;

                var delta = e.wheelDelta ? e.wheelDelta : -e.deltaY;
                var zoomFactor = delta > 0 ? 1.1 : 0.9;
                var newScale = scale * zoomFactor;

                newScale = Math.min(Math.max(0.5, newScale), 5);

                var newOffsetX = dx - imgX * newScale;
                var newOffsetY = dy - imgY * newScale;

                if (modalId === 'modal1') {{
                    scale1 = newScale;
                    offsetX1 = newOffsetX;
                    offsetY1 = newOffsetY;
                }} else if (modalId === 'modal2') {{
                    scale2 = newScale;
                    offsetX2 = newOffsetX;
                    offsetY2 = newOffsetY;
                }} else if (modalId === 'modal3') {{
                    scale3 = newScale;
                    offsetX3 = newOffsetX;
                    offsetY3 = newOffsetY;
                }}

                img.style.transform = 'translate(calc(-50% + ' + newOffsetX + 'px), calc(-50% + ' + newOffsetY + 'px)) scale(' + newScale + ')';
            }});
            
            // Pan functionality
            img.addEventListener('mousedown', function(e) {{
                e.preventDefault();
                var offsetX = modalId === 'modal1' ? offsetX1 : (modalId === 'modal2' ? offsetX2 : offsetX3);
                var offsetY = modalId === 'modal1' ? offsetY1 : (modalId === 'modal2' ? offsetY2 : offsetY3);
                startX = e.clientX - offsetX;
                startY = e.clientY - offsetY;
                isPanning = true;
                currentModalId = modalId;
            }});
            
            document.addEventListener('mousemove', function(e) {{
                if (!isPanning || currentModalId !== modalId) return;

                var scale = modalId === 'modal1' ? scale1 : (modalId === 'modal2' ? scale2 : scale3);
                var newOffsetX = e.clientX - startX;
                var newOffsetY = e.clientY - startY;

                if (modalId === 'modal1') {{
                    offsetX1 = newOffsetX;
                    offsetY1 = newOffsetY;
                }} else if (modalId === 'modal2') {{
                    offsetX2 = newOffsetX;
                    offsetY2 = newOffsetY;
                }} else if (modalId === 'modal3') {{
                    offsetX3 = newOffsetX;
                    offsetY3 = newOffsetY;
                }}

                img.style.transform = 'translate(calc(-50% + ' + newOffsetX + 'px), calc(-50% + ' + newOffsetY + 'px)) scale(' + scale + ')';
            }});
            
            document.addEventListener('mouseup', function() {{
                isPanning = false;
            }});
        }}
        
        setupZoom('modal1', 'modalImg1');
        setupZoom('modal2', 'modalImg2');
        setupZoom('modal3', 'modalImg3');
        
        // Close on Escape key
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape') {{
                closeMapModal('modal1');
                closeMapModal('modal2');
                closeMapModal('modal3');
            }}
        }});
        
        // Prevent closing when clicking on the close button
        document.querySelectorAll('.map-modal-close').forEach(function(closeBtn) {{
            closeBtn.addEventListener('click', function(e) {{
                e.stopPropagation();
            }});
        }});
        </script>
        """
        
        st.components.v1.html(maps_html, height=900, scrolling=False)
        
    elif map1_path.exists():
        st.warning("New map not found. Displaying classic map only.")
        st.image(str(map1_path), use_column_width=True)
    elif map2_path.exists():
        st.warning("Classic map not found. Displaying new map only.")
        st.image(str(map2_path), use_column_width=True)
    else:
        st.error(
            """
            **Map images not found.**
            
            Please ensure the map files exist at the correct locations.
            """
        )

    # Footer
    create_footer()


if __name__ == "__main__":
    main()
