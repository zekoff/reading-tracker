import flask
import dbhelper

application = flask.Flask(__name__)  # gunicorn looks for 'application'


@application.route('/')
def index():
    return dbhelper.get_next_reading()
