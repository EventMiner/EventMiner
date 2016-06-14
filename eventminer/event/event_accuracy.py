"""
Accuracy testing of the correct extraction of events from unstructured text.
"""
import csv
from eventminer.event.event import Event
from eventminer.event.event_formatting import convert_unicode


class CsvAccuracy(object):
    """
    CSV Table for Testing EventMiner
    Can read CSV table with test data and output accuracy
    """
    def __init__(self):
        self.filename = ""
        self.event_number = []
        # Array of events in the goldmaster file.
        self.events = []
        # 1. Event_text
        self.event_text_goldmaster = []
        self.event_text_eventminer = []
        # 2. Rule_Nr
        self.rule_nr_goldmaster = []
        self.rule_nr_eventminer = []
        # 3. Location
        self.location_goldmaster = []
        self.location_eventminer = []
        # 4. Event Start
        self.start_day_goldmaster = []
        self.start_month_goldmaster = []
        self.start_year_goldmaster = []
        self.start_day_eventminer = []
        self.start_month_eventminer = []
        self.start_year_eventminer = []
        # 5. Event End
        self.end_day_goldmaster = []
        self.end_month_goldmaster = []
        self.end_year_goldmaster = []
        self.end_day_eventminer = []
        self.end_month_eventminer = []
        self.end_year_eventminer = []

    def read_file(self, filename):
        """
        Reads CSV-goldmaster file
        """
        if self.filename != "":
            self.filename = self.filename + " + " + filename
        else:
            self.filename = filename
        # Create a reader instance
        reader = csv.reader(open(filename, 'rU'), delimiter=';', dialect=csv.excel_tab)
        # Read first line from csv file (header-information)
        fieldnames = reader.next()
        # Iterate over all other csv rows
        for row_values in reader:
            # ...and create tuples for (fieldname, fieldvalue)
            items = zip(fieldnames, row_values)
            # iterate over the created tuples
            for (fieldname, fieldvalue) in items:
                if fieldname == 'event_nr':
                    self.event_number.append(fieldvalue)
                if fieldname == "rule_nr":
                    self.rule_nr_goldmaster.append(fieldvalue)
                if fieldname == 'event_text':
                    self.event_text_goldmaster.append(fieldvalue)
                # if fieldname == 'rule_nr':
                #     self.rule_nr_goldmaster.append(fieldvalue)
                if fieldname == 'location':
                    self.location_goldmaster.append(fieldvalue)
                if fieldname == 'start_day':
                    self.start_day_goldmaster.append(fieldvalue)
                if fieldname == 'start_month':
                    self.start_month_goldmaster.append(fieldvalue)
                if fieldname == 'start_year':
                    self.start_year_goldmaster.append(fieldvalue)
                if fieldname == 'end_day':
                    self.end_day_goldmaster.append(fieldvalue)
                if fieldname == 'end_month':
                    self.end_month_goldmaster.append(fieldvalue)
                if fieldname == 'end_year':
                    self.end_year_goldmaster.append(fieldvalue)

    def extract_events(self):
        """
        Each event in the goldmaster-file is analyzed and extracted by eventminer.
        The results (extracted event, dates, etc.) will be compared with the initial data from the goldmaster-file.
        """
        for event in self.event_text_goldmaster:
            e = Event()
            e.read_text(event)
            result_set = e.start_accuracy_extraction()
            self.event_text_eventminer.append(result_set["event"].encode("utf-8"))
            self.rule_nr_eventminer.append(result_set["rule_nr"])
            self.location_eventminer.append(result_set["location"])
            self.start_day_eventminer.append(result_set["start_day"])
            self.start_month_eventminer.append(str(result_set["start_month"]))
            self.start_year_eventminer.append(result_set["start_year"])
            self.end_day_eventminer.append(str(result_set["end_day"]))
            self.end_month_eventminer.append(result_set["end_month"])
            self.end_year_eventminer.append(result_set["end_year"])

    def event_accuracy(self):
        return self.accuracy(self.event_text_goldmaster, self.event_text_eventminer,
                             self.event_number, var_name="event_text")

    def rule_accuracy(self):
        return self.accuracy(self.rule_nr_goldmaster, self.rule_nr_eventminer,
                             self.event_number, var_name="rule_id")

    def location_accuracy(self):
        return self.accuracy(self.location_goldmaster, self.location_eventminer,
                             self.event_number, var_name="location")

    def start_day_accuracy(self):
        return self.accuracy(self.start_day_goldmaster, self.start_day_eventminer,
                             self.event_number, var_name="start_day")

    def start_month_accuracy(self):
        return self.accuracy(self.start_month_goldmaster, self.start_month_eventminer,
                             self.event_number, var_name="start_month")

    def start_year_accuracy(self):
        return self.accuracy(self.start_year_goldmaster, self.start_year_eventminer,
                             self.event_number, var_name="start_year")

    def end_day_accuracy(self):
        return self.accuracy(self.end_day_goldmaster, self.end_day_eventminer,
                             self.event_number, var_name="end_day")

    def end_month_accuracy(self):
        return self.accuracy(self.end_month_goldmaster, self.end_month_eventminer,
                             self.event_number, var_name="end_month")

    def end_year_accuracy(self):
        return self.accuracy(self.end_year_goldmaster, self.end_year_eventminer,
                             self.event_number, var_name="end_year")

    def accuracy(self, array_goldmaster, array_eventminer, array_event_number, var_name):
        """
        Performs accuracy tests
            - compare length of arrays
            - compare values within the goldmaster- and eventminer-arrays
        """
        if len(array_goldmaster) != len(array_eventminer):
            # print array_goldmaster
            # print "Anzahl Elemente Goldmaster-Array: " + str(len(array_goldmaster))
            # print array_eventminer
            # print "Anzahl Elemente EventMiner Array: " + str(len(array_eventminer))
            raise ValueError("Lists must have the same length.")
        num_correct = 0
        for x, y, z in zip(array_goldmaster, array_eventminer, array_event_number):
            if str(x) == str(y):
                num_correct += 1
            else:
                print
                print "Error: "
                print "  Event:       #" + str(z)  # +1 the first line in csv are the row-descriptions
                print "  Variable:    " + var_name
                print "  Goldmaster:  " + "\"" + str(x) + "\""
                print "  Eventminer:  " + "\"" + str(y) + "\""
        return float(num_correct) / len(array_goldmaster)

    def accuracy_report(self):
        """
        Prints out an accuracy-report
        """
        self.extract_events()
        # cm = self.confusion_matrix()
        print "====================="
        print "RESULTS: "
        print "====================="
        print "Filename(s): " + self.filename
        print "Total sentences: {}".format(len(self.event_text_goldmaster))
        print
        print "EventMiner Accuracy"
        print "  Event Accuracy:            ", str(round(self.event_accuracy() * 100, 2)), '%'
        print "  Rule Accuracy:             ", str(round(self.rule_accuracy() * 100, 2)), '%'
        print "  Location Accuracy:         ", str(round(self.location_accuracy() * 100, 2)), '%'
        print "  Start Day Accuracy:        ", str(round(self.start_day_accuracy() * 100, 2)), '%'
        print "  Start Month Accuracy:      ", str(round(self.start_month_accuracy() * 100, 2)), '%'
        print "  Start Year Accuracy:       ", str(round(self.start_year_accuracy() * 100, 2)), '%'
        print "  End Day Accuracy:          ", str(round(self.end_day_accuracy() * 100, 2)), '%'
        print "  End Month Accuracy:        ", str(round(self.end_month_accuracy() * 100, 2)), '%'
        print "  End Year Accuracy:         ", str(round(self.end_year_accuracy() * 100, 2)), '%'
