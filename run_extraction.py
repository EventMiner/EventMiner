"""
This is a test-class that runs different commands.
"""
import re

import ternip
from ternip.formats.timex3 import Timex3XmlDocument

from archive import timex
from eventminer.event.event import Event
from eventminer.event.event_preprocessing import remove_references


def test_read_from_file():
    e = Event()
    e.read_file("test/test_articles/01_wikipedia_syrian_civil_war.txt")
    print e.text

#
# def test_remove_references():
#     e = Event()
#     e.read_file("test/test_articles/01_wikipedia_syrian_civil_war.txt")
#     print e.start_extraction()


def test_remove_references():
    e = Event()
    e.read_file("test/test_articles/01_wikipedia_syrian_civil_war.txt")
    text = remove_references(e.text)
    if re.search(str('\[\d{1,3}]'), text):
        print "CHECK"
    else:
        print "NO"


def test_start_extraction():
    e = Event()
    e.read_file("test/test_articles/marked_sentences.txt")
    e.start_extraction()


def test_timex():
    test_sentences = "In July 2013, the Syrian government was said to be in control of approximately 30-40% of the country's territory and 60% of the Syrian population;[110] in August 2015, the territory fully controlled by the Syrian Army was reported to have shrunk to 29,797 km2, roughly 16% of the country but still retaining the majority of the population.[111] Since October 2015, the Syrian government, backed up by direct Russian military involvement, has made significant advances both against the Islamic State of Iraq and the Levant (ISIL) and other rebels, most notably re-capturing Palmyra from the ISIL in March 2016.[112][113]"
    print timex.tag(test_sentences)
# test_timex()


def test_ternip():
    doc = Timex3XmlDocument("In July 2013, the Syrian government was said to be in control of approximately 30-40% of the country's territory and 60% of the Syrian population;[110] in August 2015, the territory fully controlled by the Syrian Army was reported to have shrunk to 29,797 km2, roughly 16% of the country but still retaining the majority of the population.[111] Since October 2015, the Syrian government, backed up by direct Russian military involvement, has made significant advances both against the Islamic State of Iraq and the Levant (ISIL) and other rebels, most notably re-capturing Palmyra from the ISIL in March 2016.[112][113]")
    rec = ternip.recogniser()
    nor = ternip.normaliser()

    print rec.tag(doc)


# test_ternip()
test_start_extraction()

