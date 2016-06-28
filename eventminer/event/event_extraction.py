"""
This class analyzes a sentence, detects and extract events.
 - If an event is detected, information for further processing (extraction) is provided.
 - For a first approach, an event is represented by a whole sentence. Later on, a sentence might be extracted into dates,
   persons, names, etc.
"""

from eventminer.event import event_formatting


# TODO: Maybe split function into smaller separated functions
# extract_events calls then "extract_date()" and after that "extract_time-range()"
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
        # -------------------------------------------
        # 1. Find whether a month or a year reference
        # -------------------------------------------

        # 1.1 Check for year-only
        # -----------------------
        if sentence.words[i].string.isdigit() and int(sentence.words[i].string) in definitions["year_range"]:
            # Exclusion of exceptions ("The 2014 FIFA World Cup took place in Brazil from 12 June 2014 to 26 June 2014")
            if not sentence.words[i+1].tag in definitions["exclusion_tags"]:
                # - assumption: a month always is referenced before a year, so when a year is found first, no
                #   month was mentioned
                time_index = i
                set_standard_result_variables(sentence, event_counter, resultset)
                resultset["start_year"] = sentence.words[i].string
                resultset["rule_nr"] = "1"
                resultset["rule_name"] = "Date: Year"

        # 1.2 Check for month-only or month and year
        # ------------------------------------------
        if sentence.words[i].string.lower() in definitions["months"].keys():
            # Try-block to avoid running into an IndexError when we reach the end of a sentence.
            # e.g. "In total, seven current FIFA officials were arrested at the Hotel Baur au Lac in Zuerich on May 27."
            try:
                # Check for exception (e.g. "... from January TILL mid 1950")
                if not sentence.words[i+1].string in definitions["keywords_time_span"]:
                    # check for year reference after month (e.g. "Feb 2015" or "Feb 3, 2015")
                    for j in range(i+1, i+4, 1):
                        # check for month and year
                        if sentence.words[j].string.isdigit() \
                                and int(sentence.words[j].string) in definitions["year_range"]:
                            time_index = j
                            set_standard_result_variables(sentence, event_counter, resultset)
                            resultset["start_month"] = definitions["months"][sentence.words[i].string.lower()]
                            resultset["start_year"] = sentence.words[j].string
                            resultset["rule_nr"] = "2"
                            resultset["rule_name"] = "Date: Month_Year"
                            break
            except IndexError:
                pass
            # if no year is found, check for month-only
            if not resultset["rule_nr"] == "2":
                time_index = i
                set_standard_result_variables(sentence, event_counter, resultset)
                resultset["start_month"] = definitions["months"][sentence.words[i].string.lower()]
                resultset["rule_nr"] = "4"
                resultset["rule_name"] = "Date: Month"

        # 1.3 Check for a day
        # -------------------
        if resultset["event_found"]:
            for k in range(time_index+1, time_index-4, -1):
                # - assumption: a day is always in the range of three positions before a month or a year,
                #   e.g. "12 Feb 2015", "30th of Feb 2015"
                # - or one position after a month, e.g. "August 29, 2012"
                if sentence.words[k].string in definitions["days"].values():
                    resultset["start_day"] = sentence.words[k].string
                    # check if year exists in order to set rules correctly
                    if resultset["start_year"]:
                        resultset["rule_nr"] = "3"
                        resultset["rule_name"] = "Date: Day_Month_Year"
                    else:
                        resultset["rule_nr"] = "4a"
                        resultset["rule_name"] = "Date: Day_Month"
                elif sentence.words[k].string in definitions["days"].keys():
                    # date-normalization: 8th -> 8
                    resultset["start_day"] = definitions["days"][sentence.words[k].string]
                    if resultset["start_year"]:
                        resultset["rule_nr"] = "3"
                        resultset["rule_name"] = "Date: Day_Month_Year"
                    else:
                        resultset["rule_nr"] = "4a"
                        resultset["rule_name"] = "Date: Day_Month"

            # -------------------------------------------------
            # 2. Check for a time-range and extract second date
            # -------------------------------------------------
            
            # 2.1 Check for time-range directly after a keyword
            # -------------------------------------------------
            if sentence.words[time_index+1].string in definitions["keywords_time_span"]:
                detect_time_range_after_keyword(definitions, resultset, sentence, time_index, time_index_2, i)
                return resultset

            try:
                if sentence.words[time_index+2].string in definitions["keywords_time_span"]:
                    # e.g. "from January 6th till mid 1950"
                    time_index += 1
                    detect_time_range_after_keyword(definitions, resultset, sentence, time_index, time_index_2, i)
                    return resultset
            except IndexError:
                pass

            # 2.2 Check for time-range when there was no keyword
            # --------------------------------------------------
            #else:
            detect_time_range_without_keyword(definitions, resultset, sentence, time_index, time_index_2, i)
                # if no keyword for a time-range was detected
                # call a function that searches the sentence through the end
                # for m in range(time_index+1, len(sentence.words), 1):
                #     print sentence.words[m].string
            return resultset


def detect_time_range_after_keyword(definitions, resultset, sentence, time_index, time_index_2, i):
    """
    Method follows basically the logic of the method above.
    After a keyword is found, the direct neighbourhood (index + 6) of the date is checked for another date.
    If a second date is found, the search is over.
    """
    try:
        for l in range(time_index + 1, time_index + 6, 1):

            # 1. Check for only end_year
            # --------------------------
            if sentence.words[l].string.isdigit() and int(sentence.words[l].string) in definitions["year_range"]:
                resultset["end_year"] = sentence.words[l].string
                # Setting of rule_numbers (according to previously set rule-numbers for a single date)

                if resultset["rule_nr"] == "4a":
                    resultset["rule_name"] = "Range: Day_Month_to_Year"
                    resultset["rule_nr"] = "6e"
                if resultset["rule_nr"] == "4":
                    resultset["rule_name"] = "Range: Month_to_Year"
                    resultset["rule_nr"] = "6d"
                if resultset["rule_nr"] in ["3", "5"]:
                    resultset["rule_name"] = "Range: Day_Month_Year_to_Year"
                    resultset["rule_nr"] = "6c"
                if resultset["rule_nr"] == "2":
                    resultset["rule_name"] = "Range: Month_Year_to_Year"
                    resultset["rule_nr"] = "6b"
                if resultset["rule_nr"] == "1":
                    resultset["rule_name"] = "Range: Year_to_Year"
                    resultset["rule_nr"] = "6a"
                # set index fur further iteration
                time_index_2 = l

            # 2. Check for month-only or month and year
            # -----------------------------------------

            #  2.1 check for month
            #  -------------------
            if sentence.words[l].string.lower() in definitions["months"].keys():
                # set index for further analysis
                time_index_2 = l
                resultset["end_month"] = definitions["months"][sentence.words[l].string.lower()]

                # 2.2 check for year reference after month (e.g. "Feb 2015" or "Feb 3, 2015")
                # ----------------------------------------
                for m in range(l + 1, l + 4, 1):

                    # check for month and year
                    if sentence.words[m].string.isdigit() and int(sentence.words[m].string) in definitions["year_range"]:
                        # resultset["end_month"] = definitions["months"][sentence.words[l].string.lower()]
                        resultset["end_year"] = sentence.words[m].string
                        time_index_2 = m

                        # print resultset["rule_nr"]

                        if resultset["rule_nr"] == "4a":
                            resultset["rule_name"] = "Range: Day_Month_to_Month_Year"
                            resultset["rule_nr"] = "7e"
                        if resultset["rule_nr"] == "4":
                            resultset["rule_name"] = "Range: Month_to_Month_Year"
                            resultset["rule_nr"] = "7d"
                        if resultset["rule_nr"] == "3":
                            resultset["rule_name"] = "Range: Day_Month_Year_to_Month_Year"
                            resultset["rule_nr"] = "7c"
                        if resultset["rule_nr"] == "2":
                            resultset["rule_name"] = "Range: Month_Year_to_Month_Year"
                            resultset["rule_nr"] = "7b"
                        if resultset["rule_nr"] == "1":
                            resultset["rule_nr"] = "7a"
                            resultset["rule_name"] = "Range: Year_to_Month_Year"

                        break
                    # check for month-only
                    # else:
                    #     time_index_2 = l
                    #     resultset["end_month"] = definitions["months"][sentence.words[i].string.lower()]
                    #     break


            # 3. Check for a day
            # ------------------
            if time_index_2:

                for n in range(time_index_2 - 1, time_index_2 - 4, -1):
                    # Exception: "from January 6th till mid 1950"
                    if sentence.words[n].string in definitions["keywords_time_span"]:
                        break

                    # - assumption: a day is always in the range of three positions before a month or a year,
                    #   e.g. "12 Feb 2015", "30th of Feb 2015"
                    if sentence.words[n].string in definitions["days"].values():
                        resultset["end_day"] = sentence.words[n].string

                        #print resultset["rule_nr"]
                        if resultset["rule_nr"] == "7d":
                            resultset["rule_nr"] = "8d"
                            resultset["rule_name"] = "Range: Month_to_Day_Month_Year"
                        if resultset["rule_nr"] == "7c":
                            resultset["rule_nr"] = "8c"
                            resultset["rule_name"] = "Range: Day_Month_Year_to_Day_Month_Year"
                        if resultset["rule_nr"] == "7b":
                            resultset["rule_nr"] = "8b"
                            resultset["rule_name"] = "Range: Month_Year_to_Day_Month_Year"
                        if resultset["rule_nr"] == "7a":
                            resultset["rule_nr"] = "8a"
                            resultset["rule_name"] = "Range: Year_to_Day_Month_Year"
                    elif sentence.words[n].string in definitions["days"].keys():
                        # date-normalization: 8th -> 8
                        resultset["end_day"] = definitions["days"][sentence.words[n].string]
                        if resultset["rule_nr"] == "7d":
                            resultset["rule_nr"] = "8d"
                            resultset["rule_name"] = "Range: Month_to_Day_Month_Year"
                        if resultset["rule_nr"] == "7c":
                            resultset["rule_nr"] = "8c"
                            resultset["rule_name"] = "Range: Day_Month_Year_to_Day_Month_Year"
                        if resultset["rule_nr"] == "7b":
                            resultset["rule_nr"] = "8b"
                            resultset["rule_name"] = "Range: Month_Year_to_Day_Month_Year"
                        if resultset["rule_nr"] == "7a":
                            resultset["rule_nr"] = "8a"
                            resultset["rule_name"] = "Range: Year_to_Day_Month_Year"
    except IndexError:
        pass


def detect_time_range_without_keyword(definitions, resultset, sentence, time_index, time_index_2, i):

    return resultset

def set_standard_result_variables(sentence, counter, resultset):
    resultset["event_found"] = True
    resultset["event_nr"] = counter
    resultset["event"] = event_formatting.remove_blanks(sentence.string)
