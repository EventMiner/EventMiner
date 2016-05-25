"""
This is a parser that converts the output of different taggers (like pattern, spacy) into a standardized format.
This enables switching between different parsers and corrects some mistakes of the taggers (e.g. Pattern adds
blanks after symbols).
"""
from sentence import Sentence
from word import Word
from eventminer.event.event_formatting import remove_blanks
from pattern.en import parse, Text
from spacy.en import English


def convert_into_eventminer_format(text, tagger="pattern"):
    """
    Input: some text
    Type of tagger: "pattern" or "spacy"
    Eventminer-Format: defined in classes Sentence and Word
    """
    # parse pattern-output into eventminer-format
    if tagger == "pattern":
        return convert_pattern_format(text)
    # parse spacy-output into eventminer-format
    if tagger == "spacy":
        return convert_spacy_format(text)
    return


def convert_pattern_format(text):
    """
    Text is parsed through pattern's parsing function into a standardized format.
    """
    parsed_text = []
    # parse text via Pattern's parser
    pattern_parsed_text = Text(parse(text, relations=True, lemmata=True))
    for sentence in pattern_parsed_text:
        s = Sentence()
        s.string = remove_blanks(sentence.string)
        for word in sentence:
            # Patterns tags for each word in the sentence are stored in a new Word-object
            w = Word()
            w.string = word.string
            w.lemma = word.lemma
            w.index = word.index
            w.tag = word.type
            w.entity = ""
            # each word is appended to a Sentence-object
            s.words.append(w)
        # each Sentence-object is appended to an array
        parsed_text.append(s)
    return parsed_text


def convert_spacy_format(text):
    parsed_text = []
    # instantiate Spacy's parser
    parser = English()
    # parse text via Spacy's parser
    doc = parser(unicode(text, "utf-8"))
    for sent in doc.sents:
        s = Sentence()
        s.string = str(sent)
        word_index = 0
        for token in sent:
            # problem: sometimes, spacy interprets a new line in a text-file wrongly and provides an empty token.
            # solved: by the following condition
            if len(token.orth_) > 1:
                # Spacy's tags for each word in the sentence are stored in a new Word-object
                w = Word()
                w.string = token.orth_
                w.lemma = token.lemma_
                w.index = word_index
                # less verbose tags are provided by "token.pos_"
                w.tag = token.tag_
                w.entity = token.ent_type_
                word_index += 1
                # each word is appended to a Sentence-object
                s.words.append(w)
        # each Sentence-object is appended to an array
        parsed_text.append(s)
    return parsed_text
