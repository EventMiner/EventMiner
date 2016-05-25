"""
This class holds functions that clean the text that comes from distributed sources.
 - e.g. cleaning of references from Wikipedia articles.
"""
import re


def remove_references(text):
    """
    Remove references from text that are stated in square brackets with a number, e.g. "[123]"
    """
    cleaned_text = re.sub(str('\[\d{1,3}]'), "", text)

    # remove ; from text and replace them with a '.'
    cleaned_text = re.sub(str(";"), ".", cleaned_text)

    return cleaned_text
