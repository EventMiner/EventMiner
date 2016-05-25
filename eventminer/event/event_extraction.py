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
                 "start_date_day": "",
                 "start_date_month": "",
                 "start_date_year": "",
                 "end_date_day": "",
                 "end_date_month": "",
                 "end_date_year": ""}

    for i in range(0, len(sentence.words), 1):
        # Search for a yearly reference in a given range
        if sentence.words[i].string.isdigit() and sentence.words[i].string.isdigit() in definitions["year_range"]:

            # RULE: Time-span from X to Y (e.g. "From 1958 to 1961, a brief union...")
            if sentence.words[i+1].string in definitions["keywords_time_span"]:

                # Case: from year to year
                if sentence.words[i+2].string.isdigit():
                    resultset["event_found"] = True
                    resultset["event_nr"] = event_counter
                    resultset["start_date_year"] = sentence.words[i].string
                    resultset["end_date_year"] = sentence.words[i+2].string
                    resultset["event"] = sentence.string
                    return resultset

                # Case: from month-year to month-year
                if sentence.words[i-1].string.lower() in definitions["months"] \
                        and sentence.words[i+2].string.lower() in definitions["months"]:
                    resultset["event_found"] = True
                    resultset["event_nr"] = event_counter
                    resultset["start_date_month"] = definitions["months"][sentence.words[i-1].string.lower()]
                    resultset["start_date_year"] = sentence.words[i].string
                    resultset["end_date_month"] = definitions["months"][sentence.words[i+2].string.lower()]
                    resultset["end_date_year"] = sentence.words[i+3].string
                    resultset["event"] = sentence.string
                    return resultset

            # RULE: Seasonal Reference (e.g. "early spring of 2013")
            if sentence.words[i-1].string == "of":
                resultset["event_found"] = True
                resultset["event_nr"] = event_counter
                resultset["start_date_year"] = sentence.words[i].string
                resultset["event"] = sentence.string
                return resultset

            # RULE: Date surrounded by commas (e.g. "December, 2012,")
            if sentence.words[i-1].string == "," and sentence.words[i+1].string == ",":
                resultset["event_found"] = True
                resultset["event_nr"] = event_counter
                resultset["start_date_year"] = sentence.words[i].string
                resultset["event"] = sentence.string
                # check for mentioning of a month
                if sentence.words[i-2].string.lower() in definitions["months"]:
                    resultset["start_date_month"] = definitions["months"][sentence.words[i-2].string.lower()]
                return resultset

            # RULE: Keywords in front of a year (e.g. "in 2012")
            if sentence.words[i-1].string.lower() in definitions["keywords_year"]:

                # Case: ended in year
                if sentence.words[i-2].string == "ended":
                    resultset["event_found"] = True
                    resultset["event_nr"] = event_counter
                    resultset["end_date_year"] = sentence.words[i].string
                    resultset["event"] = sentence.string
                    return resultset

                resultset["event_found"] = True
                resultset["event_nr"] = event_counter
                resultset["start_date_year"] = sentence.words[i].string
                resultset["event"] = sentence.string
                return resultset

            # RULE: Keywords in front of a month (e.g. "In September 2012" or "On 30 September 2013")
            if sentence.words[i-1].string.lower() in definitions["months"]:

                # Check for mentioning of a day
                if sentence.words[i-2].string.isdigit() and int(sentence.words[i-2].string) in definitions["day_range"]:
                    resultset["event_found"] = True
                    resultset["event_nr"] = event_counter
                    resultset["start_date_day"] = int(sentence.words[i-2].string)
                    resultset["start_date_month"] = definitions["months"][sentence.words[i-1].string.lower()]
                    resultset["start_date_year"] = sentence.words[i].string
                    resultset["event"] = sentence.string
                    return resultset

                # Case: ended in month-year
                if sentence.words[i-3].string == "ended":
                    resultset["event_found"] = True
                    resultset["event_nr"] = event_counter
                    resultset["end_date_month"] = definitions["months"][sentence.words[i-1].string.lower()]
                    resultset["end_date_year"] = sentence.words[i].string
                    resultset["event"] = sentence.string
                    return resultset

                # If no day-number is present, just extract the month
                else:
                    resultset["event_found"] = True
                    resultset["event_nr"] = event_counter
                    resultset["start_date_month"] = definitions["months"][sentence.words[i-1].string.lower()]
                    resultset["start_date_year"] = sentence.words[i].string
                    resultset["event"] = sentence.string
                    return resultset

    return resultset
