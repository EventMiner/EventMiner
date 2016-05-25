"""
Unit tests for class event.py
"""

from nose.tools import *
from eventminer.event.event import Event


def test_read_from_file_should_deliver_text():
    """
    Test, if reading a file returns a string that is not empty.
    """
    e = Event()
    e.read_file("test/test_articles/01_wikipedia_syrian_civil_war.txt")
    assert_not_equal(e.text, "")
