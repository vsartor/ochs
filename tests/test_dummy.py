"""
Test dummy module.
"""

from ochs import greet

def test_dummy() -> None:
    assert greet("me") == "Hello, me."
