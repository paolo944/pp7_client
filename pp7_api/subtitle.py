import requests
import json, jsonify

class Subtitle:
    def __init__(self):
        with open('info.json', 'r') as config_file:
            config = json.load(config_file)
            self.url = f'{config["url"]}status/'

    def update(self):
        headers = {
            'Content-Type': 'application/json',
            'accept': 'application/json'
        }

        data = [
            "playlist/active",
            "status/slide"
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
        data = {"type": None, "subtitle": None}
        for chunk in response.iter_content(chunk_size=1):
            buffer += chunk
            if b'\r\n\r\n' in buffer:
                lines = buffer.split(b'\r\n\r\n')
                for line in lines[:-1]:
                    if line:
                        try:
                            data["subtitle"] = ""
                            json_line = json.loads(line.decode('utf-8'))
                            if(json_line["url"] == "playlist/active"):
                                if("Louange" in json_line["data"]["presentation"]["playlist"]["name"]):
                                    data["type"] = "louange"
                                elif("Versets" in json_line["data"]["presentation"]["playlist"]["name"]):
                                    data["type"] = "versets"
                            elif(json_line["url"] == "status/slide"):
                                if(data["type"] == "louange"):
                                    paroles = json_line["data"]["current"]["text"].split('\n')
                                    paroles = [paroles[i] for i in range(0, len(paroles), 2)]
                                    paroles = '\n'.join(paroles)
                                    data["subtitle"] = paroles
                                elif(data["type"] == "versets"):
                                    paroles = json_line["data"]["current"]["text"]
                                    data["subtitle"] = paroles
                                json_output = json.dumps(data)
                                print(data)
                                yield f"data: {json_output}\n\n"
                        except json.JSONDecodeError:
                            print(f"Erreur de décodage JSON pour la ligne : {line}")
                buffer = lines[-1]
