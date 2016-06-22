#!/usr/bin/env python

from flask import Flask, jsonify, render_template, request
from eventminer.event.event import Event
from eventminer.event.event_accuracy import CsvAccuracy
import run_accuracy, run_extraction

# Create the application
app = Flask(__name__)

@app.route('/accuracy')
def accuracy():
    result = run_accuracy.test_start_accuracy()
    return jsonify(accuracy_result=result)

@app.route('/extraction')
def extraction():
    #wiki_link = request.args.get('wiki_link', "", type=str)
    result = run_extraction.test_start_extraction()
    return jsonify(extraction_result=result)

@app.route('/')
def index():
    """Displays the index page accessible at '/'
        """
    return render_template('index.html')

if __name__ == '__main__':
    app.debug=True
    app.run()