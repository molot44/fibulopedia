"""
Unit tests for fibula_status service.
"""

import pytest
from src.services.fibula_status import _parse_online_from_html


# Sample HTML fixture with the relevant structure
SAMPLE_HTML_WITH_COUNT = """
<!DOCTYPE html>
<html>
<body>
    <section id="sidebar-misc">
        <a href="https://amera.fibula.app/online">Players online</a>
        <div class="line"></div>
        <a href="https://amera.fibula.app/online">
            Amera&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;694
        </a>
        <div class="line"></div>
    </section>
</body>
</html>
"""

SAMPLE_HTML_WITHOUT_COUNT = """
<!DOCTYPE html>
<html>
<body>
    <section id="sidebar-misc">
        <a href="https://amera.fibula.app/online">Players online</a>
        <div class="line"></div>
        <a href="https://amera.fibula.app/online">
            Amera
        </a>
        <div class="line"></div>
    </section>
</body>
</html>
"""

SAMPLE_HTML_NO_SECTION = """
<!DOCTYPE html>
<html>
<body>
    <div>No sidebar here</div>
</body>
</html>
"""


def test_parse_online_from_html_success():
    """Test that the parser correctly extracts the online player count."""
    result = _parse_online_from_html(SAMPLE_HTML_WITH_COUNT)
    assert result == 694


def test_parse_online_from_html_no_number():
    """Test that the parser returns None when there's no number."""
    result = _parse_online_from_html(SAMPLE_HTML_WITHOUT_COUNT)
    assert result is None


def test_parse_online_from_html_no_section():
    """Test that the parser returns None when the section is missing."""
    result = _parse_online_from_html(SAMPLE_HTML_NO_SECTION)
    assert result is None


def test_parse_online_from_html_empty_string():
    """Test that the parser handles empty HTML gracefully."""
    result = _parse_online_from_html("")
    assert result is None


def test_parse_online_from_html_malformed():
    """Test that the parser handles malformed HTML gracefully."""
    result = _parse_online_from_html("<html><body>malformed")
    assert result is None
