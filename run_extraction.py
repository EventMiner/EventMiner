"""
This is a test-class that runs different commands.
"""
import re

from eventminer.event.event import Event
from eventminer.event.event_preprocessing import remove_references


def test_read_from_file():
    e = Event()
    e.read_file("test/test_articles/random_test.txt")
    print(e.text)


def test_remove_references():
    e = Event()
    e.read_file("test/test_articles/01_wikipedia_syrian_civil_war.txt")
    text = remove_references(e.text)
    if re.search(str('\[\d{1,3}]'), text):
        print("CHECK")
    else:
        print("NO")


def test_start_extraction():
    e = Event()
    e.read_file("test/test_articles/random_test.txt")
    e.start_extraction()


def flask_start_extraction(wiki_text):
    e = Event()
    e.text = wiki_text
    e.text = remove_references(e.text)
    return e.start_extraction()

test_start_extraction()
