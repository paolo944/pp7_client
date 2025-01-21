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
        data = {"type": None}
        for chunk in response.iter_content(chunk_size=1):
            buffer += chunk
            if b'\r\n\r\n' in buffer:
                lines = buffer.split(b'\r\n\r\n')
                for line in lines[:-1]:
                    if line:
                        try:
                            data["subtitle"] = None
                            data["ref"] = None
                            data["versets"] = None
                            json_line = json.loads(line.decode('utf-8'))
                            if(json_line["url"] == "status/slide"):
                                text = json_line["data"]["current"]["text"]
                                data["type"] = "versets" if any(char.isdigit() for char in text) else "louanges"
                                if(data["type"] == "louanges"):
                                    paroles = text.split('\n')
                                    paroles = [paroles[i] for i in range(0, len(paroles), 2)]
                                    paroles = '\n'.join(paroles)
                                    data["subtitle"] = paroles
                                elif(data["type"] == "versets"):
                                    text = text.split('\n\n')[0]
                                    ref = text.split('\n')[0]
                                    versets = text.split('\n')[1]
                                    data["ref"] = ref
                                    data["versets"] = versets
                                json_output = json.dumps(data)
                                print(data)
                                yield f"data: {json_output}\n\n"
                        except json.JSONDecodeError:
                            print(f"Erreur de décodage JSON pour la ligne : {line}")
                buffer = lines[-1]
