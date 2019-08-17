from flask import Flask, render_template
import dbhelper

application = Flask(__name__)  # gunicorn looks for 'application'


@application.route('/')
def index():
    return render_template('index.html', passage=dbhelper.get_next_reading())
