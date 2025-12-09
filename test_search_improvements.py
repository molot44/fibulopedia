"""
Test script for improved search functionality.
Tests search with page routes and clickable results.
"""

from src.services.search_service import search_all, get_page_route

def test_search_with_routes():
    """Test that search results include page routes"""
    print("=" * 70)
    print("SEARCH IMPROVEMENTS TEST")
    print("=" * 70)
    print()
    
    # Test 1: Search for "dragon"
    print("Test 1: Search for 'dragon'")
    results = search_all("dragon")
    print(f"Found {len(results)} results")
    print()
    
    for i, result in enumerate(results[:5], 1):
        print(f"{i}. {result.name}")
        print(f"   Type: {result.entity_type}")
        print(f"   ID: {result.entity_id}")
        print(f"   Snippet: {result.snippet[:80]}..." if len(result.snippet) > 80 else f"   Snippet: {result.snippet}")
        print(f"   Page Route: {result.page_route}")
        print()
    
    # Test 2: Test page route mapping
    print("=" * 70)
    print("Test 2: Page Route Mapping")
    print("=" * 70)
    print()
    
    entity_types = ["weapon", "equipment", "spell", "monster", "quest", "food", "tool"]
    for entity_type in entity_types:
        route = get_page_route(entity_type)
        print(f"{entity_type.title():15} -> {route}")
    print()
    
    # Test 3: Verify all results have routes
    print("=" * 70)
    print("Test 3: Verify All Results Have Routes")
    print("=" * 70)
    print()
    
    test_queries = ["sword", "shield", "fire", "rat", "thais"]
    for query in test_queries:
        results = search_all(query)
        missing_routes = [r for r in results if not r.page_route]
        status = "✓ OK" if len(missing_routes) == 0 else f"✗ FAIL ({len(missing_routes)} missing)"
        print(f"Query '{query}': {len(results)} results, {status}")
    
    print()
    print("=" * 70)
    print("TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    test_search_with_routes()
