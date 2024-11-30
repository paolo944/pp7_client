import requests
import json

class Playlist:
    def __init__(self, name):
        with open('info.json', 'r') as config_file:
            config = json.load(config_file)
            self.url = config["url"]
        
        headers = {
            'Content-Type': 'application/json',
            'accept': 'application/json'
        }

        data = {
            'name': name,
            'type': 'playlist'
        }

        json_data = json.dumps(data)

        response = requests.post(f"{self.url}playlists", headers=headers, data=json_data)

        if response.status_code == 200:
            self.id = response.json()["id"]
        else:
            print(f'Échec de la requête. Code de statut : {response.status_code}')

    def get_id(self):
        print(f"Playlist: {self.id["name"]}, index: {self.id["index"]}, uuid: {self.id["uuid"]}")