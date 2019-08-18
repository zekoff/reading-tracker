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
    _, passage, week = dbhelper.get_next_reading()
    submitted_data = request.form.get('time_spent', None)
    if submitted_data is not None:
        try:
            submitted_data = int(submitted_data)
            dbhelper.complete_reading(submitted_data)
        except Exception as ex:
            logger.error(ex)
            submitted_data = "Error submitting data"
    logger.debug(f'Form data (if submitted): {submitted_data}')
    template_vars = {
        'passage': passage,
        'week': week,
        'submitted_data': submitted_data
    }
    return render_template('index.html', **template_vars)
