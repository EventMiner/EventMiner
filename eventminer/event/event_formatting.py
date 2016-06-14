import re


def convert_unicode(text):
    """
    Unfortunately, Spacy works only with unicode-strings which leads to a strange output for special signs, like
    "approximately 30\u201340% of the country's..."
    For adequate output, these unicode has to be replaced with human-readable letters.
    """
    cleaned_text = text.replace('\\u2013', '-')
    return cleaned_text


def remove_blanks(sentence_string):
    """
    Removes blanks before and after special characters which are caused by patterns (not so great) parsing process.

    """
    a = re.compile(' ,')
    b = re.compile(' \'')
    c = re.compile('\( ')
    d = re.compile(' \)')
    e = re.compile(' ;')
    f = re.compile(' :')
    g = re.compile(' \.')
    h = re.compile(' n\'t')
    i = re.compile('\[ ')
    j = re.compile(' \]')
    # k = re.compile('" ')
    # l = re.compile(' "')
    m = re.compile(str("\' "))

    if a.search(sentence_string):
        sentence_string = a.sub(',', sentence_string)
    if b.search(sentence_string):
        sentence_string = b.sub('\'', sentence_string)
    if c.search(sentence_string):
        sentence_string = c.sub(('('), sentence_string)
    if d.search(sentence_string):
        sentence_string = d.sub((')'), sentence_string)
    if e.search(sentence_string):
        sentence_string = e.sub(';', sentence_string)
    if f.search(sentence_string):
        sentence_string = f.sub(':', sentence_string)
    if g.search(sentence_string):
        sentence_string = g.sub(('.'), sentence_string)
    if h.search(sentence_string):
        sentence_string = h.sub('n\'t', sentence_string)
    if i.search(sentence_string):
        sentence_string = i.sub(('['), sentence_string)
    if j.search(sentence_string):
        sentence_string = j.sub((']'), sentence_string)
    # if k.search(sentence_string):
    #     sentence_string = k.sub(('"'), sentence_string)
    # if l.search(sentence_string):
    #     sentence_string = l.sub(('" '), sentence_string)
    if m.search(sentence_string):
        sentence_string = m.sub(str("\'"), sentence_string)

    return sentence_string
