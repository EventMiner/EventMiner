#!/usr/bin/env python

from flask import Flask, jsonify, render_template, request
from eventminer.event.event import Event
from eventminer.event.event_accuracy import CsvAccuracy
import run_accuracy, run_extraction
import requests
from HTMLParser import HTMLParser

# Create the application
app = Flask(__name__)

@app.route('/accuracy')
def accuracy():
    result = run_accuracy.test_start_accuracy()
    return jsonify(accuracy_result=result)

@app.route('/extraction')
def extraction():
    term = request.args.get('term', "", type=str)
    #url = "https://en.wikipedia.org/w/api.php?action=opensearch&format=json&search=" + term
    #url = "https://en.wikipedia.org/w/api.php?action=query&titles="+term+"&prop=revisions&rvprop=content&format=json"
    url = "https://en.wikipedia.org/w/api.php?action=query&titles="+term+"&prop=extracts&format=json"
    data = requests.get(url)
    array = data.json()
    text_id = array['query']['pages'].keys()[0].encode('ascii','ignore')
    wiki_text = array['query']['pages'][text_id]['extract']
    wiki_text = strip_tags(wiki_text)

    result = run_extraction.flask_start_extraction(wiki_text)
    return jsonify(extraction_result=result)

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

if __name__ == '__main__':
    app.debug=True
    app.run()
