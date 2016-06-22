"""
Defines CSV-Files for accuracy-tests.
"""

from eventminer.event.event_accuracy import CsvAccuracy

def test_start_accuracy():
    c = CsvAccuracy()
    c.read_file("csv/goldmaster_event.csv")

    return c.accuracy_report()