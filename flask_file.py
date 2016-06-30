#!/usr/bin/env python

from flask import Flask, jsonify, render_template, request
import run_accuracy, run_extraction
import requests
import urllib2

# Create the application
app = Flask(__name__)

@app.route('/accuracy')
def accuracy():
    result = run_accuracy.test_start_accuracy()
    return jsonify(accuracy_result=result)

@app.route('/extraction', methods=['GET', 'POST'])
def extraction():
    wiki_text = request.json['text']
    wiki_text = urllib2.unquote(wiki_text)
    try:
        result = run_extraction.flask_start_extraction(wiki_text)
        return jsonify(extraction_result=result)
    except:
        return jsonify(extraction_result=[])


if __name__ == '__main__':
    app.debug=True
    app.run()
