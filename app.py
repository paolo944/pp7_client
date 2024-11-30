from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from pp7_api import stage, stream

stage = stage.Stage()
stream = stream.Stream()

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

if __name__ == '__main__':
    app.run(debug=True)