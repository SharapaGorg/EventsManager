from sys import argv
from utils import logger
from flask import Flask, jsonify, request
from flask_cors import CORS
from database import get_events, add_event

app = Flask(__name__)
CORS(app)

if len(argv) == 1:
    logger.warning("--dev || --prod argument expected")
    exit()

if argv[1] == '--dev':
    mode = 'dev'
    HOST, PORT = '127.0.0.1', 5000

elif argv[1] == '--prod':
    mode  = 'prod'
    HOST, PORT = 'something', 4001

else:
    logger.warning("--dev || --prod argument excpected", f"Got : '{argv[1]}'")
    exit()

@app.route('/', methods=['GET'])
def root():
    return '<h1>Docs will be here</h1>'

@app.route('/events', methods=['GET', 'POST'])
def get_events_():
    try:
        data = request.get_json()

        start = finish = None

        if data:
            start : float = data.get('start')
            finish : float = data.get('finish')

        events = get_events(start, finish)
        return jsonify(events)

    except Exception as e:
        return str(e), 400

@app.route('/add_event', methods=['POST'])
def add_event_():
    try:
        data = request.get_json()

        title : str = data.get('title')
        link  : str = data.get('link')
        description : str = data.get('description')
        start : float = data.get('start')
        finish : float = data.get('finish')

        add_event(title, link, description, start, finish)

        return 'success'

    except Exception as e:
        return str(e), 400

app.run(host=HOST, port=PORT, debug=True)