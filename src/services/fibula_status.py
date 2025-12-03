"""
Fibula Status Service - Fetches online player count from the Fibula Project server.

This module scrapes the MyAAC website to retrieve the current number of players online.
"""

import re
import requests
from bs4 import BeautifulSoup
from typing import Optional

from src.logging_utils import setup_logger

logger = setup_logger(__name__)

# URL to fetch the player count from
STATUS_URL = "https://amera.fibula.app/news"


def _parse_online_from_html(html: str) -> Optional[int]:
    """
    Parse the HTML content to extract the online player count.
    
    This function looks for a section with id="sidebar-misc" and extracts
    the player count from an anchor tag containing the server name "Amera".
    
    Args:
        html: The HTML content as a string.
        
    Returns:
        The number of online players as an int, or None if parsing fails.
    """
    try:
        soup = BeautifulSoup(html, "html.parser")
        
        # Find the sidebar-misc section
        sidebar_misc = soup.find("section", id="sidebar-misc")
        if not sidebar_misc:
            logger.warning("Could not find section with id='sidebar-misc'")
            return None
        
        # Find all <a> tags with href to the online page
        online_links = sidebar_misc.find_all("a", href="https://amera.fibula.app/online")
        
        # Look for the link containing the server name and player count
        for link in online_links:
            text = link.get_text()
            if "Amera" in text:
                # Remove whitespace and non-breaking spaces
                clean_text = text.replace("\xa0", " ").strip()
                
                # Extract the last number using regex
                match = re.search(r"(\d+)$", clean_text)
                if match:
                    return int(match.group(1))
        
        logger.warning("Could not find online player count in HTML")
        return None
        
    except Exception as e:
        logger.error(f"Error parsing HTML: {e}")
        return None


def fetch_online_count() -> Optional[int]:
    """
    Fetch the current number of players online on the Amera (Fibula) server
    by scraping the MyAAC website sidebar.
    
    This function performs an HTTP request to the Fibula Project website,
    parses the HTML, and extracts the online player count from the sidebar.
    
    Returns:
        The number of online players as an int, or None if it cannot be determined.
        
    Examples:
        >>> count = fetch_online_count()
        >>> if count is not None:
        ...     print(f"Players online: {count}")
    """
    try:
        # Headers to avoid being blocked as a bot
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Fetch the HTML with a timeout
        response = requests.get(STATUS_URL, headers=headers, timeout=5)
        response.raise_for_status()
        
        # Parse and extract the player count
        return _parse_online_from_html(response.text)
        
    except requests.Timeout:
        logger.error("Timeout while fetching online player count")
        return None
    except requests.RequestException as e:
        logger.error(f"Network error while fetching online player count: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching online player count: {e}")
        return None
