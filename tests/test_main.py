"""
Tests for the main module.
"""

from song_graph.main import greet

def test_greet():
    """Test the greet function."""
    # Given
    name = "Alice"
    expected = "Hello, Alice! Welcome to Song-Graph."
    
    # When
    result = greet(name)
    
    # Then
    assert result == expected 