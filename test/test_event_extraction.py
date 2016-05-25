"""
Unit Tests for Event Extraction
"""

from nose.tools import *
from eventminer.event.event import Event


def test_correct_amount_of_events_should_be_extracted():
    """
    Test, if all events of the test-file marked_sentences.txt are extracted
    """
    e = Event()
    e.read_file("test/test_articles/marked_sentences.txt")
    assert_equal(len(e.start_extraction()), 19)
