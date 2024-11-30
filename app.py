from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from pp7_api import stage, stream, timer

stage = stage.Stage()
stream = stream.Stream()
timer = timer.Timer()

app = Flask(__name__)

# Route pour la page d'accueil
@app.route('/')
def home():
    return render_template('index.html')

# Route pour obtenir des données de l'API
@app.route('/stage/send_msg', methods=['PUT'])
def stage_send_msg():
    data = request.get_json()
    msg = data.get('user_input')
    result = stage.send_msg(msg)
    return jsonify({'result': result})

@app.route('/stage/delete_msg', methods=['DELETE'])
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

if __name__ == '__main__':
    app.run(debug=True)