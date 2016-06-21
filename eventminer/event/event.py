"""
This class analyzes an article (e.g. from Wikipedia) and conducts the extraction process.
 1) article is read
 2) article is parsed into an array of sentences
 3) each sentence is analyzed whether or not it contains an event
 4) if a sentence contains an event, it is written into a csv-file
"""
from eventminer.event import event_preprocessing
import eventminer.res.dic_definitions
from eventminer.parser import parser
from eventminer.event import event_extraction


class Event(object):
    """
    Analyzes text and stores extracted events.
    """
    # load dictionary
    definitions = eventminer.res.dic_definitions.dic_definitions

    def __init__(self):
        self.filename = ""
        self.text = ""
        self.parsed_text = []
        self.event_list = []

    def read_text(self, textstring):
        """
        Reads event from String. Needed for accuracy-testing.
        """
        self.text = textstring

    def read_file(self, filename):
        """
        Reads a text file and saves the content in the property text
        """
        with open(filename) as f:
            self.filename = filename
            self.text = f.read()
            f.close()

    def start_extraction(self):
        """
        Starts the extraction of events from text.
        """
        # 1. Pre-process text in order to improve parsing
        self.text = event_preprocessing.remove_references(self.text)
        # 2. Parse article into sentence-objects
        self.parsed_text = parser.convert_into_eventminer_format(self.text, tagger="pattern")
        # 3. Analyze every sentence in text, if it contains an event
        event_counter = 1
        for sentence in self.parsed_text:
            try:
                resultset = event_extraction.extract_event(sentence, Event.definitions, event_counter)
                # check, if an event is extracted from the sentence
                if resultset["event_found"]:
                    # print variables for testing and more verbose information:
                    print("---------------")
                    print("Event_Nr:     " + str(resultset["event_nr"]))
                    print("Rule_Nr:      " + str(resultset["rule_nr"]))
                    print("Rule_Name:    " + str(resultset["rule_name"]))
                    print("Event:        " + resultset["event"])
                    print("Start Day:    " + str(resultset["start_day"]))
                    print("Start Month:  " + str(resultset["start_month"]))
                    print("Start Year:   " + str(resultset["start_year"]))
                    print("End Day:      " + str(resultset["end_day"]))
                    print("End Month:    " + str(resultset["end_month"]))
                    print("End Year:     " + str(resultset["end_year"]))
                    # append result-dic to a list
                    self.event_list.append(event_extraction.extract_event(sentence, Event.definitions, event_counter))
                    event_counter += 1
            except TypeError:
                pass

        return self.event_list

    def start_accuracy_extraction(self):
        """
        Starting function for the accuracy-report that compares a goldmaster corpus with the results of eventminer.
        This is a test-comment.
        """
        self.text = event_preprocessing.remove_references(self.text)
        # parse hypotheses from csv-file
        self.parsed_text = parser.convert_into_eventminer_format(self.text, tagger="pattern")
        event_counter = 1
        for sentence in self.parsed_text:
            resultset = event_extraction.extract_event(sentence, Event.definitions, event_counter)
            event_counter += 1
            return resultset
