import sys
import logging
from flask import Flask, render_template, request
import dbhelper

application = Flask(__name__)  # gunicorn looks for 'application'
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

@application.route('/', methods=['GET', 'POST'])
def index():
    submitted_data = False
    if request.method == 'POST':
        try:
            dbhelper.complete_reading()
            submitted_data = True
        except Exception as ex:
            logger.error(ex)
    reading_id, passage, week = dbhelper.get_next_reading()
    template_vars = {
        'passage': passage,
        'week': week,
        'submitted_data': submitted_data,
        'accept_input': (reading_id != None)
    }
    return render_template('index.html', **template_vars)
