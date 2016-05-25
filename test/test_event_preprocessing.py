"""
Unit tests for class event_preprocessing.py
"""
from nose.tools import *
from eventminer.event.event import Event
from eventminer.event.event_preprocessing import *


def test_references_should_be_removed():
    """
    Check, if references are removed from text.
    Maybe to be refined later on, because, it is the same regex command that removes the references from text -
    therefore it is most likely that this test is fine. hmm...
    """
    e = Event()
    e.read_file("test/test_articles/01_wikipedia_syrian_civil_war.txt")
    # re searches for references in bracktes, like "[12]" and should not find any.
    assert_false(re.search(str('\[\d{1,3}]'), remove_references(e.text)))
