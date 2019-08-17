from flask import Flask, render_template, request
import dbhelper

application = Flask(__name__)  # gunicorn looks for 'application'


@application.route('/')
def index():
    return render_template('index.html', passage=dbhelper.get_next_reading())

@application.route('/record_reading')
def record_reading():
    return request.form['time_spent']