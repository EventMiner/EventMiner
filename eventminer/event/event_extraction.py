"""
This class analyzes a sentence, detects and extract events.
 - If an event is detected, information for further processing (extraction) is provided.
 - For a first approach, an event is represented by a whole sentence. Later on, a sentence might be extracted into dates,
   persons, names, etc.
"""


# TODO: Maybe split funtion into smaller separated functions
# extract_events calls then "extract_date()" and after that "extract_timespan()"
def extract_event(sentence, definitions, event_counter):
    """
    Analyzes a sentence, if it contains an event.
        1. Check for time-spans (the occurence of more than one date in text)
        2. Check for time-points
    """
    # storing of results of the extraction process
    resultset = {"rule_nr": "",
                 "rule_name": "",
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

    # time_index of relevant year or month, whichever was found
    # time_index_2 is for the second date, after a range was detected
    time_index = 0
    time_index_2 = 0

    for i in range(0, len(sentence.words), 1):
        # print event_counter
        # print sentence.words[i].string, sentence.words[i].tag
        # print sentence.string

        # -------------------------------------------
        # 1. Find whether a month or a year reference
        # -------------------------------------------
        # 1.1 check for year-only
        if sentence.words[i].string.isdigit() and int(sentence.words[i].string) in definitions["year_range"]:

            # Exclusion of exceptions ("The 2014 FIFA World Cup took place in Brazil from 12 June 2014 to 26 June 2014")
            if not sentence.words[i+1].tag in definitions["exclusion_tags"]:
                # - assumption: a month always is referenced before a year, so when a year is found first, no
                #   month was mentioned
                time_index = i
                set_standard_result_variables(sentence, event_counter, resultset)
                resultset["start_year"] = sentence.words[i].string
                resultset["rule_nr"] = 1
                resultset["rule_name"] = "Date: Year"

        # 1.2 check for month-only or month and year
        if sentence.words[i].string.lower() in definitions["months"].keys():
            # Try-block to avoid running into an IndexError when we reach the end of a sentence.
            # e.g. "In total, seven current FIFA officials were arrested at the Hotel Baur au Lac in Zuerich on May 27."
            try:
                # check for year reference after month (e.g. "Feb 2015" or "Feb 3, 2015")
                for j in range(i+1, i+4, 1):
                    # check for month and year
                    if sentence.words[j].string.isdigit() \
                            and int(sentence.words[j].string) in definitions["year_range"]:
                        time_index = j
                        set_standard_result_variables(sentence, event_counter, resultset)
                        resultset["start_month"] = definitions["months"][sentence.words[i].string.lower()]
                        resultset["start_year"] = sentence.words[j].string
                        resultset["rule_nr"] = 2
                        resultset["rule_name"] = "Date: Year_Month"
                        break
            except IndexError:
                pass

            # if no year is found, check for month-only
            if not resultset["rule_nr"] == 2:
                time_index = i
                set_standard_result_variables(sentence, event_counter, resultset)
                resultset["start_month"] = definitions["months"][sentence.words[i].string.lower()]


        if resultset["event_found"]:

            # 1.3 Check for a day
            for k in range(time_index+1, time_index-4, -1):
                # - assumption: a day is always in the range of three positions before a month or a year,
                #   e.g. "12 Feb 2015", "30th of Feb 2015"
                # - or one position after a month, e.g. "August 29, 2012"
                if sentence.words[k].string in definitions["days"].values():
                    resultset["start_day"] = sentence.words[k].string
                    # check if year exists in order to set rules correctly
                    if resultset["start_year"]:
                        resultset["rule_nr"] = 3
                        resultset["rule_name"] = "Date: Year_Month_Day"
                    else:
                        resultset["rule_nr"] = 4
                        resultset["rule_name"] = "Date: Month_Day"
                elif sentence.words[k].string in definitions["days"].keys():
                    # date-normalization: 8th -> 8
                    resultset["start_day"] = definitions["days"][sentence.words[k].string]
                    if resultset["start_year"]:
                        resultset["rule_nr"] = 3
                        resultset["rule_name"] = "Date: Year_Month_Day"
                    else:
                        resultset["rule_nr"] = 4
                        resultset["rule_name"] = "Date: Month_Day"

            # -------------------------------------------
            # 2. Check for a timespan and extract second date
            # -----------------------------------------------
            if sentence.words[time_index+1].string in definitions["keywords_time_span"]:
                # use the logic of detecting months and years from above
                for l in range(time_index+1, len(sentence.words), 1):
                    # 2.1 check for year-only
                    if sentence.words[l].string.isdigit() and int(sentence.words[l].string) in definitions["year_range"]:
                        time_index_2 = l
                        resultset["end_year"] = sentence.words[l].string
                    # 2.2 check for month-only or month and year
                    if sentence.words[l].string.lower() in definitions["months"].keys():
                        # check for year reference after month (e.g. "Feb 2015" or "Feb 3, 2015")
                        for m in range(l+1, l+3, 1):
                            # check for month and year
                            if sentence.words[m].string.isdigit() and int(sentence.words[m].string) in definitions["year_range"]:
                                time_index_2 = m
                                resultset["end_month"] = definitions["months"][sentence.words[l].string.lower()]
                                resultset["end_year"] = sentence.words[m].string
                                break
                            # check for month-only
                            else:
                                time_index_2 = l
                                resultset["end_month"] = definitions["months"][sentence.words[i].string.lower()]
                                break
                    # 2.3 Check for a day
                    if time_index_2:
                        for n in range(time_index_2-1, time_index_2-4, -1):
                            # - assumption: a day is always in the range of three positions before a month or a year,
                            #   e.g. "12 Feb 2015", "30th of Feb 2015"
                            if sentence.words[n].string in definitions["days"].values():
                                resultset["end_day"] = sentence.words[n].string
                            elif sentence.words[n].string in definitions["days"].keys():
                                # date-normalization: 8th -> 8
                                resultset["end_day"] = definitions["days"][sentence.words[n].string]

            return resultset


def set_standard_result_variables(sentence, counter, resultset):
    resultset["event_found"] = True
    resultset["event_nr"] = counter
    resultset["event"] = sentence.string
