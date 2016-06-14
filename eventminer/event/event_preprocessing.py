"""
This class holds functions that clean the text that comes from distributed sources.
 - e.g. cleaning of references from Wikipedia articles.
"""
import re


def remove_references(text):
    """
    some text pre-formatting
    """
    # Remove references from text that are stated in square brackets with a number, e.g. "[123]"
    cleaned_text = re.sub(str('\[\d{1,3}]'), "", text)

    # remove ; from text and replace them with a '.'
    cleaned_text = re.sub(str(";"), ".", cleaned_text)

    # remove " from text, because patterns algorithm causes trouble otherwise. If necessary, a different
    # workaround can be developed
    cleaned_text = re.sub(str("\""), "", cleaned_text)

    # replace "-" between years, because Pattern get confused otherwise...
    cleaned_text = re.sub(r'(\d{2,4})(-)(\d{2,4})', r'\1 to \3', cleaned_text)

    return cleaned_text
