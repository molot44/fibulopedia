"""
Travel Calculator page for Fibulopedia.

This page calculates the best and cheapest travel routes between cities.
"""

import streamlit as st
from typing import List, Tuple, Dict, Optional
import heapq

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
setup_page_config("Travel Calculator", "🗺️")
load_custom_css()
create_sidebar_navigation("Travel Calculator")


# Travel routes with costs (based on the screenshot)
# Format: {(from, to): cost}
BOAT_ROUTES = {
    ("Ab'Dendriel", "Carlin"): 80,
    ("Ab'Dendriel", "Edron"): 70,
    ("Ab'Dendriel", "Thais"): 130,
    ("Ab'Dendriel", "Venore"): 90,
    
    ("Carlin", "Ab'Dendriel"): 80,
    ("Carlin", "Thais"): 110,
    ("Carlin", "Venore"): 130,
    
    ("Darashia", "Venore"): 60,
    
    ("Edron", "Ab'Dendriel"): 70,
    ("Edron", "Carlin"): 110,
    ("Edron", "Venore"): 40,
    
    ("Thais", "Ab'Dendriel"): 130,
    ("Thais", "Carlin"): 110,
    ("Thais", "Venore"): 170,
    
    ("Venore", "Ab'Dendriel"): 90,
    ("Venore", "Carlin"): 130,
    ("Venore", "Darashia"): 60,
    ("Venore", "Edron"): 40,
    ("Venore", "Thais"): 170,
}

# Carpet routes (optional)
CARPET_ROUTES = {
    ("Edron Carpet", "Femor Hills Carpet"): 60,
    ("Edron Carpet", "Darashia Carpet"): 40,
    ("Femor Hills Carpet", "Edron Carpet"): 60,
    ("Femor Hills Carpet", "Darashia Carpet"): 80,
    ("Darashia Carpet", "Edron Carpet"): 40,
    ("Darashia Carpet", "Femor Hills Carpet"): 80,
}

# Special connections
# Carlin to Ice Islands (Folda, Senja, Vega) - 20 gp with free return
ICE_ISLANDS = ["Folda", "Senja", "Vega"]
CARLIN_TO_ICE_ISLANDS = 20  # One way, return is free

# City aliases for carpet connections
CARPET_CITIES = {
    "Edron": "Edron Carpet",
    "Darashia": "Darashia Carpet",
    "Femor Hills": "Femor Hills Carpet"
}

ALL_CITIES = [
    "Ab'Dendriel", "Carlin", "Darashia", "Edron", 
    "Thais", "Venore", "Folda", "Senja", "Vega", "Femor Hills", "Kazordoon"
]


def build_graph(include_carpets: bool) -> Dict[str, List[Tuple[str, int]]]:
    """Build adjacency list graph from routes."""
    graph = {}
    
    # Add boat routes
    for (from_city, to_city), cost in BOAT_ROUTES.items():
        if from_city not in graph:
            graph[from_city] = []
        graph[from_city].append((to_city, cost))
    
    # Add Ice Islands routes from Carlin
    if "Carlin" not in graph:
        graph["Carlin"] = []
    for island in ICE_ISLANDS:
        graph["Carlin"].append((island, CARLIN_TO_ICE_ISLANDS))
        # Return from Ice Islands to Carlin is free
        if island not in graph:
            graph[island] = []
        graph[island].append(("Carlin", 0))
    
    # Add walking connections between Femor Hills, Carlin, and Kazordoon (nearby locations)
    nearby_cities = [("Femor Hills", "Carlin"), ("Femor Hills", "Kazordoon"), ("Carlin", "Kazordoon")]
    for city1, city2 in nearby_cities:
        if city1 not in graph:
            graph[city1] = []
        if city2 not in graph:
            graph[city2] = []
        # Free walking connections both ways
        graph[city1].append((city2, 0))
        graph[city2].append((city1, 0))
    
    # Add carpet routes if enabled
    if include_carpets:
        for (from_city, to_city), cost in CARPET_ROUTES.items():
            if from_city not in graph:
                graph[from_city] = []
            graph[from_city].append((to_city, cost))
        
        # Connect Edron and Darashia to their carpets (carpets are IN the cities, so free access)
        for city in ["Edron", "Darashia"]:
            carpet = f"{city} Carpet"
            if city not in graph:
                graph[city] = []
            if carpet not in graph:
                graph[carpet] = []
            # Free bidirectional connection
            graph[city].append((carpet, 0))
            graph[carpet].append((city, 0))
        
        # Femor Hills Carpet is accessible from Carlin (walking distance)
        if "Femor Hills Carpet" not in graph:
            graph["Femor Hills Carpet"] = []
        if "Carlin" not in graph:
            graph["Carlin"] = []
        graph["Carlin"].append(("Femor Hills Carpet", 0))
        graph["Femor Hills Carpet"].append(("Carlin", 0))
    
    return graph


def find_all_routes(graph: Dict[str, List[Tuple[str, int]]], start: str, end: str, max_routes: int = 5) -> List[Tuple[int, List[str]]]:
    """Find multiple routes using modified Dijkstra to explore different paths."""
    if start not in graph:
        return []
    
    # Priority queue: (cost, current_city, path, visited_set)
    pq = [(0, start, [start], frozenset([start]))]
    found_routes = []
    route_signatures = set()  # To avoid duplicate routes
    
    while pq and len(found_routes) < max_routes:
        cost, current, path, visited = heapq.heappop(pq)
        
        if current == end:
            # Create signature to identify unique routes (based on path structure)
            signature = tuple(path)
            if signature not in route_signatures:
                route_signatures.add(signature)
                found_routes.append((cost, path))
            continue
        
        if current in graph:
            for neighbor, edge_cost in graph[current]:
                if neighbor not in visited:
                    new_cost = cost + edge_cost
                    new_path = path + [neighbor]
                    new_visited = visited | {neighbor}
                    heapq.heappush(pq, (new_cost, neighbor, new_path, new_visited))
    
    # Sort by cost
    found_routes.sort(key=lambda x: x[0])
    
    # Check if there are direct routes (after filtering out city<->carpet transitions, only 1 real step)
    direct_routes = []
    for cost, path in found_routes:
        # Count real steps (excluding Edron/Darashia <-> their Carpet transitions)
        real_steps = 0
        for i in range(len(path) - 1):
            from_city = path[i]
            to_city = path[i + 1]
            # Skip city<->carpet transitions
            if not ((from_city == "Edron" and to_city == "Edron Carpet") or 
                    (from_city == "Edron Carpet" and to_city == "Edron") or 
                    (from_city == "Darashia" and to_city == "Darashia Carpet") or 
                    (from_city == "Darashia Carpet" and to_city == "Darashia")):
                real_steps += 1
        
        if real_steps == 1:
            direct_routes.append((cost, path))
    
    # If there are direct routes, return only those (both boat and carpet if available)
    if direct_routes:
        return direct_routes[:2]  # Max 2: one boat, one carpet
    
    # Otherwise, return shortest route(s)
    if len(found_routes) <= 2:
        return found_routes
    
    filtered_routes = [found_routes[0]]  # Always include cheapest
    
    # Look for a carpet route that's different from the cheapest
    for cost, path in found_routes[1:]:
        uses_carpet = any("Carpet" in city for city in path)
        cheapest_uses_carpet = any("Carpet" in city for city in found_routes[0][1])
        
        # Add if it's a carpet route and cheapest wasn't, or vice versa
        if uses_carpet != cheapest_uses_carpet:
            filtered_routes.append((cost, path))
            break
    
    return filtered_routes


def dijkstra(graph: Dict[str, List[Tuple[str, int]]], start: str, end: str) -> Tuple[Optional[int], Optional[List[str]]]:
    """Find cheapest path using Dijkstra's algorithm."""
    routes = find_all_routes(graph, start, end, max_routes=1)
    if routes:
        return routes[0]
    return None, None


def format_route(path: List[str], graph: Dict[str, List[Tuple[str, int]]]) -> List[Dict[str, any]]:
    """Format route with individual leg costs, skipping city<->carpet transitions for Edron and Darashia."""
    if not path or len(path) < 2:
        return []
    
    legs = []
    skip_next = False
    
    for i in range(len(path) - 1):
        if skip_next:
            skip_next = False
            continue
            
        from_city = path[i]
        to_city = path[i + 1]
        
        # Skip Edron/Darashia <-> their Carpet transitions (free walk within city)
        if (from_city == "Edron" and to_city == "Edron Carpet") or \
           (from_city == "Edron Carpet" and to_city == "Edron") or \
           (from_city == "Darashia" and to_city == "Darashia Carpet") or \
           (from_city == "Darashia Carpet" and to_city == "Darashia"):
            continue
        
        # Find cost for this leg
        cost = 0
        if from_city in graph:
            for neighbor, edge_cost in graph[from_city]:
                if neighbor == to_city:
                    cost = edge_cost
                    break
        
        # Determine transport type
        transport = "⛵ Boat"
        if from_city in CARPET_CITIES.values() or to_city in CARPET_CITIES.values():
            if cost == 0:
                transport = "🚶 Walk"
            else:
                transport = "🪂 Carpet"
        elif from_city == "Carlin" and to_city in ICE_ISLANDS:
            transport = "⛵ Boat"
        elif from_city in ICE_ISLANDS and to_city == "Carlin":
            transport = "⛵ Boat (Free Return)"
        
        legs.append({
            "from": from_city,
            "to": to_city,
            "cost": cost,
            "transport": transport
        })
    
    return legs


def main() -> None:
    """Main function to render the travel calculator page."""
    logger.info("Rendering travel calculator page")

    # Page header
    create_page_header(
        title="Travel Calculator",
        subtitle="Find the cheapest route between cities",
        icon=""
    )

    st.markdown("### Plan Your Journey")
    
    # Input section
    col1, col2 = st.columns(2)
    
    with col1:
        from_city = st.selectbox(
            "Travel From",
            options=["Select city..."] + sorted(ALL_CITIES),
            index=0,
            help="Select your starting city"
        )
    
    with col2:
        to_city = st.selectbox(
            "Travel To",
            options=["Select city..."] + sorted(ALL_CITIES),
            index=0,
            help="Select your destination"
        )
    
    include_carpets = st.checkbox(
        "Include carpet routes",
        value=True,
        help="Enable magic carpet travel between Edron, Darashia, and Femor Hills"
    )
    
    st.markdown("---")
    
    # Calculate route
    if from_city and to_city and from_city != "Select city..." and to_city != "Select city...":
        if from_city == to_city:
            st.warning("⚠️ Starting city and destination are the same!")
        else:
            # Build graph and find all routes
            graph = build_graph(include_carpets)
            all_routes = find_all_routes(graph, from_city, to_city, max_routes=10)
            
            if all_routes:
                st.success(f"✅ Found {len(all_routes)} route option(s)")
                
                # Display each route variant
                st.markdown("### 🛤️ Available Routes")
                
                for variant_num, (total_cost, path) in enumerate(all_routes, 1):
                    # Format route details
                    legs = format_route(path, graph)
                    
                    # Create visual route display
                    route_html = f"""
                    <style>
                    .route-container {{
                        background: linear-gradient(135deg, rgba(30,30,30,0.95), rgba(40,40,40,0.95));
                        border: 2px solid #d4af37;
                        border-radius: 12px;
                        padding: 1.5rem;
                        margin: 1rem 0;
                    }}
                    .variant-header {{
                        font-size: 1.2rem;
                        color: #d4af37;
                        font-weight: bold;
                        margin-bottom: 1rem;
                        padding-bottom: 0.5rem;
                        border-bottom: 1px solid #d4af37;
                    }}
                    .route-leg {{
                        display: flex;
                        align-items: center;
                        justify-content: space-between;
                        padding: 0.75rem;
                        margin: 0.5rem 0;
                        background: rgba(50,50,50,0.5);
                        border-radius: 8px;
                        border-left: 3px solid #d4af37;
                    }}
                    .route-cities {{
                        flex: 1;
                        font-size: 1rem;
                        color: #e0e0e0;
                    }}
                    .city-name {{
                        color: #d4af37;
                        font-weight: bold;
                    }}
                    .route-arrow {{
                        margin: 0 0.5rem;
                        color: #888;
                    }}
                    .route-cost {{
                        font-size: 1.1rem;
                        font-weight: bold;
                        color: #50c878;
                        min-width: 80px;
                        text-align: right;
                    }}
                    .route-cost.free {{
                        color: #4a90e2;
                    }}
                    .route-transport {{
                        font-size: 0.9rem;
                        color: #aaa;
                        margin-left: 1rem;
                        min-width: 100px;
                    }}
                    .total-cost {{
                        margin-top: 1rem;
                        padding: 1rem;
                        background: linear-gradient(135deg, rgba(80,200,120,0.2), rgba(80,200,120,0.1));
                        border: 2px solid #50c878;
                        border-radius: 8px;
                        text-align: center;
                        font-size: 1.3rem;
                        font-weight: bold;
                        color: #50c878;
                    }}
                    </style>
                    <div class="route-container">
                        <div class="variant-header">Option {variant_num}</div>
                    """
                    
                    for i, leg in enumerate(legs, 1):
                        cost_class = "free" if leg["cost"] == 0 else ""
                        cost_text = "Free" if leg["cost"] == 0 else f"{leg['cost']} gp"
                        
                        route_html += f"""
                        <div class="route-leg">
                            <div class="route-cities">
                                <span style="color: #888; font-size: 0.85rem;">Step {i}:</span>
                                <span class="city-name">{leg['from']}</span>
                                <span class="route-arrow">→</span>
                                <span class="city-name">{leg['to']}</span>
                            </div>
                            <div class="route-transport">{leg['transport']}</div>
                            <div class="route-cost {cost_class}">{cost_text}</div>
                        </div>
                        """
                    
                    route_html += f"""
                        <div class="total-cost">
                            Total Cost: {total_cost} gp
                        </div>
                    </div>
                    """
                    
                    st.components.v1.html(route_html, height=min(200 + len(legs) * 80, 600), scrolling=True)
            else:
                st.error("❌ No route found between these cities!")
                st.info("Try enabling carpet routes or check if the cities are connected.")

    # Footer
    st.markdown("""
        <div style='text-align: center; color: #888; font-size: 0.9rem;'>
            <p>💰 Prices based on Fibula Project (Tibia 7.1)</p>
            <p>Routes calculated using boat services and optional magic carpets</p>
        </div>
    """, unsafe_allow_html=True)
    
    create_footer()


if __name__ == "__main__":
    main()
