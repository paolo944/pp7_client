from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from flask_socketio import SocketIO, emit, join_room, leave_room
from pp7_api import stage, stream, timer, subtitle
import requests, json
from threading import Thread
import time

stage = stage.Stage()
stream = stream.Stream()
timer = timer.Timer()
subtitle = subtitle.Subtitle()

app = Flask(__name__)

socketio = SocketIO(app)

sse_clients = {}

# Route pour la page d'accueil
@app.route('/')
def home():
    return render_template('index.html')

# Route pour obtenir des données de l'API
@app.route('/stage/msg', methods=['PUT'])
def stage_send_msg():
    data = request.get_json()
    msg = data.get('user_input')
    result = stage.send_msg(msg)
    return jsonify({'result': result})

@app.route('/stage/msg', methods=['DELETE'])
def stage_delete_msg():
    result = stage.delete_msg()
    return jsonify({'result': result})

@app.route('/current_status_stream')
def current_status_stream():
    return Response(stream.stream_update(), mimetype="text/event-stream")

@app.route('/timer/play/<string:uuid>', methods=['GET'])
def play_timer(uuid):
    result = timer.play(uuid)
    return jsonify({'result': result})

@app.route('/timer/pause/<string:uuid>', methods=['GET'])
def pause_timer(uuid):
    result = timer.pause(uuid)
    return jsonify({'result': result})

@app.route('/timer/reset/<string:uuid>', methods=['GET'])
def reset_timer(uuid):
    result = timer.reset(uuid)
    return jsonify({'result': result})

@app.route('/timer/<string:uuid>', methods=['DELETE'])
def delete_timer(uuid):
    result = timer.delete(uuid)
    return jsonify({'result': result})

@app.route('/timer/<string:uuid>', methods=['PUT'])
def modify_timer(uuid):
    result = timer.modify(uuid)
    return jsonify({'result': result})

@app.route('/timer', methods=['POST'])
def post_timer():
    data = request.get_json()
    hours = data.get('hours')
    minutes = data.get('minutes')
    seconds = data.get('seconds')
    print(f"Received time: {hours}:{minutes}:{seconds}")
    result = timer.post(data)
    return jsonify({'result': result})

@app.route('/joke', methods=['GET'])
def joke():
    with open('info.json', 'r') as config_file:
        config = json.load(config_file)
        url = f'{config["url"]}find_my_mouse'
    print(url)
    headers = {
        'accept': '*/*'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 204:
        return jsonify({'result': 'True'})
    else:
        print(f'Échec de la requête Joke. Code de statut : {response.status_code}')
        return jsonify({'result': 'False'})
    
@app.route("/subtitles", methods=['GET'])
def index():
    return render_template("subtitles.html")

@app.errorhandler(400)
def bad_request(error):
    app.logger.error(f"Bad request: {request.data}")
    return jsonify({'message': 'Bad request'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)