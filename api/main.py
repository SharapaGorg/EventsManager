import datetime
from sys import argv
from flask import Flask, jsonify, request
from flask_cors import CORS
from database import *
from utils import get_user_by_jwt, logger

app = Flask(__name__)
CORS(app)

if len(argv) == 1:
    logger.warning("--dev || --prod argument expected")
    exit()

if argv[1] == '--dev':
    mode = 'dev'
    HOST, PORT = '127.0.0.1', 5000

elif argv[1] == '--prod':
    mode = 'prod'
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

        start = finish = topic_id = None

        if data:
            start: float = data.get('start')
            finish: float = data.get('finish')
            topic_id : int = data.get('topic_id')
            date : str = data.get('date')
            jwt : str = data.get('JWT')
        
        user = get_user_by_jwt(jwt)
        events = get_events(user['id'], date, start, finish, topic_id)
        return jsonify(events)

    except Exception as e:
        logger.error(e)
        return str(e), 400


@app.route('/topics', methods=['GET', 'POST'])
def get_topics_():
    try:
        data = request.get_json()

        title = None

        if data:
            title = data.get('title')
            jwt = data.get('JWT')

        user = get_user_by_jwt(jwt)
        topics = get_topics(user['id'], title)

        return jsonify(topics)

    except Exception as e:
        logger.error(e)
        return str(e), 400


@app.route('/event', methods=['POST'])
def get_concrete_event_():
    try:
        data = request.get_json()
        event_id = data['id']

        event = get_event(event_id)
        return jsonify(event)

    except Exception as e:
        return str(e), 400


@app.route('/add_event', methods=['POST'])
def add_event_():
    try:
        data = request.get_json()

        title: str = data.get('title')
        link: str = data.get('link')
        description: str = data.get('description')
        start: float = data.get('start')
        finish: float = data.get('finish')
        topic_id : int = data.get('topic_id')
        date : str = data.get('date')
        jwt : str = data.get('JWT')

        user = get_user_by_jwt(jwt)

        add_event(title, date, link, description, start, finish, topic_id, user['id'])

        return 'success'

    except Exception as e:
        logger.error(e)
        return str(e), 400

@app.route('/update_event', methods=['POST'])
def update_event_():
    try:
        data = request.get_json()

        jwt : str = data.get('JWT')
        id : float = data.get('event_id')
        start : float = data.get('start')
        finish : float = data.get('finish')

        user = get_user_by_jwt(jwt)
        update_event(id, start, finish, user['id'])

        return 'success'

    except Exception as e:
        logger.error(e)
        return str(e), 400

@app.route('/add_topic', methods=['POST'])
def add_topic_():
    try:
        data = request.get_json()

        title : str = data.get('title')
        jwt : str = data.get('JWT')

        user = get_user_by_jwt(jwt)

        add_topic(user['id'], title)
        return 'success'

    except Exception as e:
        logger.error(e)
        return str(e), 400

@app.route('/login', methods=['POST'])
def login_():
    try:
        data = request.get_json()

        login: str = data.get('login')
        password: str = data.get('password')

        login_attempt = login_user(login, password)
        if login_attempt:
            return {
                "message" : "???????????????? ????????!",
                "status" : "SUCCESS",
                "token" : login_attempt
            }

        return {
            "message": "???????????????????????? ????????????, ???????????????????? ?????? ??????!",
            "status" : "FAIL"
        }

    except Exception as e:
        logger.error(e)
        return "??????-???? ?????????? ???? ??????", 400


@app.route('/register', methods=['POST'])
def register_():
    try:
        data = request.get_json()

        login: str = data.get('login')
        password: str = data.get('password')

        attempt = add_user(login, password)

        if not attempt:
            return {
                "message" : "?????????????? ?? ?????????? ???????????? ?????? ????????????????????(",
                "status" : "FAIL",
            }

        return {
            "message" : f"{login}, ?????????????? ?? ???????? ??????????????????????????!",
            "status" : "SUCCESS",
            "token" : attempt
        }

    except Exception as e:
        logger.error(e)
        return "??????-???? ?????????? ???? ??????", 400

@app.route('/user', methods=['POST'])
def get_user_info_():
    try:
        data = request.get_json()

        jwt = data.get('JWT')

        if jwt is None:
            return {}

        user = get_user_by_jwt(jwt)
        user['password'] = 'NO-READABLE'

        return user

    except Exception as e:
        logger.error(e)
        return str(e), 400

start = datetime.datetime.now() - datetime.timedelta(hours=1)
finish = start + datetime.timedelta(hours=4)

# add_event("???????????? ???? ??????", "12/11/2022", "https://jut.su/", "???????????????? ???????????????? ????????", start.timestamp(), finish.timestamp(), 3, 1)

app.run(host=HOST, port=PORT, debug=True)