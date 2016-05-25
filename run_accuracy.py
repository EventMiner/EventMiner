"""
Defines CSV-Files for accuracy-tests.
"""

from eventminer.event.event_accuracy import CsvAccuracy

c = CsvAccuracy()
c.read_file("csv/goldmaster_event.csv")

c.accuracy_report()
