import requests
import json

class Stream:
    def __init__(self):
        with open('info.json', 'r') as config_file:
            config = json.load(config_file)
            self.url = f'{config["url"]}status/'

    def stream_update(self):
        headers = {
            'Content-Type': 'application/json',
            'accept': 'application/json'
        }

        data = [
            "stage/message",
            "timers/current",
            "timer/video_countdown",
            "timer/system_time",
            "status/slide",
            "presentation/active"
        ]

        json_data = json.dumps(data)

        response = requests.post(f'{self.url}updates', headers=headers, data=json_data, stream=True)

        if response.status_code == 400:
            print(f'Échec de la requête Status. Code de statut : {response.status_code}')
            yield jsonify({'data': "400"})
            return
        elif response.status_code == 404:
            print(f'Application ProPresenter non détécté')
            yield jsonify({'data': "404"})
            return

        buffer = b''
        for chunk in response.iter_content(chunk_size=1):
            buffer += chunk
            if b'\r\n\r\n' in buffer:
                lines = buffer.split(b'\r\n\r\n')
                for line in lines[:-1]:
                    if line:
                        try:
                            json_line = json.loads(line.decode('utf-8'))
                            if(json_line["url"] == "presentation/active"):
                                if(json_line["data"]["presentation"] != None):
                                    json_line["data"] = json_line["data"]["presentation"]["id"]["name"]
                            json_output = json.dumps(json_line)
                            yield f"data: {json_output}\n\n"
                        except json.JSONDecodeError:
                            print(f"Erreur de décodage JSON pour la ligne : {line}")
                buffer = lines[-1]

#curl -X POST -H "Content-Type: application/json" -H "accept: application/json" -d '["timer/system_time", "stage/message", "timers/current", "timer/video_countdown", "timer/system_time"]' http://192.168.1.124:4020/v1/status/updates