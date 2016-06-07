"""
This class analyzes a sentence, detects and extract events.
 - If an event is detected, information for further processing (extraction) is provided.
 - For a first approach, an event is represented by a whole sentence. Later on, a sentence might be extracted into dates,
   persons, names, etc.
"""


def extract_event(sentence, definitions, event_counter):
    """
    Analyzes a sentence, if it contains an event.
        1. Check for time-spans (the occurence of more than one date in text)
        2. Check for time-points
    """
    # storing of results of the extraction process
    resultset = {"rule_nr": "",
                 "event_found": False,
                 "event_nr": "",
                 "event": "",
                 "location": "",
                 "start_day": "",
                 "start_month": "",
                 "start_year": "",
                 "end_day": "",
                 "end_month": "",
                 "end_year": ""}
    # for checking if month or year was initially found
    # if year == False, only a month was detected
    only_year = False
    only_month = False
    timespan = False
    timespan_index = 0

    for i in range(0, len(sentence.words), 1):

        # 1. Find whether a month or a year reference
        # 1.1 check for year-only
        if sentence.words[i].string.isdigit() and int(sentence.words[i].string) in definitions["year_range"]:
            # - assumption: a month always is referenced before a year, so when a year is found first, no
            #   month was mentioned
            only_year = True
            set_standard_result_variables(sentence, event_counter, resultset)
            resultset["start_year"] = sentence.words[i].string

        # 1.2 check for month-only or month and year
        if sentence.words[i].string.lower() in definitions["months"].keys():
            # check for year reference after month (e.g. "Feb 2015" or "Feb 3, 2015")
            for j in range(i+1, i+3, 1):
                # check for month and year
                if sentence.words[j].string.isdigit() and int(sentence.words[j].string) in definitions["year_range"]:
                    month_and_year = True
                    set_standard_result_variables(sentence, event_counter, resultset)
                    resultset["start_month"] = definitions["months"][sentence.words[i].string.lower()]
                    resultset["start_year"] = sentence.words[j].string
                # check for month-only
                else:
                    only_month = True
                    set_standard_result_variables(sentence, event_counter, resultset)
                    resultset["start_month"] = definitions["months"][sentence.words[i].string.lower()]

        # 2. Check for a timespan
        if resultset["event_found"]:
            



        #
        # print sentence.words[i].string.lower()
        # if month:
        #     print "CHECK"
        #     break


        # resultset["event_found"] = True
        # resultset["event_nr"] = event_counter
        # resultset["event"] = sentence.string
        # resultset["start_month"] = sentence.words[i].string









            # Rule 1:   "From YMD till YMD"
            # Example:  "from 8 February 1904 - 5 September 1905"
            # if sentence.words[i-1].string.lower() in definitions["months"].keys() and \
            #                 sentence.words[i-2].string in definitions["days"].values():
            #     print "Check"



        # # Search for a yearly reference in a given range
        # if sentence.words[i].string.isdigit() and sentence.words[i].string.isdigit() in definitions["year_range"]:
        #
        #     # RULE: Time-span from X to Y (e.g. "From 1958 to 1961, a brief union...")
        #     if sentence.words[i+1].string in definitions["keywords_time_span"]:
        #
        #         # Case: from year to year
        #         if sentence.words[i+2].string.isdigit():
        #             resultset["rule_nr"] = 1
        #             resultset["event_found"] = True
        #             resultset["event_nr"] = event_counter
        #             resultset["start_date_year"] = sentence.words[i].string
        #             resultset["end_date_year"] = sentence.words[i+2].string
        #             resultset["event"] = sentence.string
        #             return resultset
        #
        #         # Case: from month-year to month-year
        #         if sentence.words[i-1].string.lower() in definitions["months"] \
        #                 and sentence.words[i+2].string.lower() in definitions["months"]:
        #             resultset["rule_nr"] = 2
        #             resultset["event_found"] = True
        #             resultset["event_nr"] = event_counter
        #             resultset["start_date_month"] = definitions["months"][sentence.words[i-1].string.lower()]
        #             resultset["start_date_year"] = sentence.words[i].string
        #             resultset["end_date_month"] = definitions["months"][sentence.words[i+2].string.lower()]
        #             resultset["end_date_year"] = sentence.words[i+3].string
        #             resultset["event"] = sentence.string
        #             return resultset
        #
        #     # RULE: Seasonal Reference (e.g. "early spring of 2013")
        #     if sentence.words[i-1].string == "of":
        #         resultset["rule_nr"] = 3
        #         resultset["event_found"] = True
        #         resultset["event_nr"] = event_counter
        #         resultset["start_date_year"] = sentence.words[i].string
        #         resultset["event"] = sentence.string
        #         return resultset
        #
        #     # RULE: Date surrounded by commas (e.g. "December, 2012,")
        #     if sentence.words[i-1].string == "," and sentence.words[i+1].string == ",":
        #         resultset["rule_nr"] = 4
        #         resultset["event_found"] = True
        #         resultset["event_nr"] = event_counter
        #         resultset["start_date_year"] = sentence.words[i].string
        #         resultset["event"] = sentence.string
        #         # check for mentioning of a month
        #         if sentence.words[i-2].string.lower() in definitions["months"]:
        #             resultset["rule_nr"] = 5
        #             resultset["start_date_month"] = definitions["months"][sentence.words[i-2].string.lower()]
        #         return resultset
        #
        #     # RULE: Keywords in front of a year (e.g. "in 2012")
        #     if sentence.words[i-1].string.lower() in definitions["keywords_year"]:
        #
        #         # Case: ended in year
        #         if sentence.words[i-2].string == "ended":
        #             resultset["rule_nr"] = 6
        #             resultset["event_found"] = True
        #             resultset["event_nr"] = event_counter
        #             resultset["end_date_year"] = sentence.words[i].string
        #             resultset["event"] = sentence.string
        #             return resultset
        #
        #         resultset["rule_nr"] = 7
        #         resultset["event_found"] = True
        #         resultset["event_nr"] = event_counter
        #         resultset["start_date_year"] = sentence.words[i].string
        #         resultset["event"] = sentence.string
        #         return resultset
        #
        #     # RULE: Keywords in front of a month (e.g. "In September 2012" or "On 30 September 2013")
        #     if sentence.words[i-1].string.lower() in definitions["months"]:
        #
        #         # Check for mentioning of a day
        #         if sentence.words[i-2].string.isdigit() and int(sentence.words[i-2].string) in definitions["day_range"]:
        #             resultset["rule_nr"] = 8
        #             resultset["event_found"] = True
        #             resultset["event_nr"] = event_counter
        #             resultset["start_date_day"] = int(sentence.words[i-2].string)
        #             resultset["start_date_month"] = definitions["months"][sentence.words[i-1].string.lower()]
        #             resultset["start_date_year"] = sentence.words[i].string
        #             resultset["event"] = sentence.string
        #             return resultset
        #
        #         # Case: ended in month-year
        #         if sentence.words[i-3].string == "ended":
        #             resultset["rule_nr"] = 9
        #             resultset["event_found"] = True
        #             resultset["event_nr"] = event_counter
        #             resultset["end_date_month"] = definitions["months"][sentence.words[i-1].string.lower()]
        #             resultset["end_date_year"] = sentence.words[i].string
        #             resultset["event"] = sentence.string
        #             return resultset
        #
        #         # If no day-number is present, just extract the month
        #         else:
        #             print sentence.words[i].string
        #             print sentence.words[i-1].string
        #             resultset["rule_nr"] = 10
        #             resultset["event_found"] = True
        #             resultset["event_nr"] = event_counter
        #             resultset["start_date_month"] = definitions["months"][sentence.words[i-1].string.lower()]
        #             resultset["start_date_year"] = sentence.words[i].string
        #             resultset["event"] = sentence.string
        #             return resultset


    return resultset


def set_standard_result_variables(sentence, counter, resultset):
    resultset["event_found"] = True
    resultset["event_nr"] = counter
    resultset["event"] = sentence.string
